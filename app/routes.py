from app import app, login_manager
from flask import render_template, request, redirect, url_for, flash, send_file
from .models import User
from flask_login import logout_user, login_required, login_user, current_user
from .config import os, Config
from .generate import generate
from .execute import execute
from .upload_file import upload_file
import ast

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_entry = request.form.get('username')
        user = User.query.filter((User.username == form_entry) | (User.email == form_entry)).first()
        if user is None or not user.check_password(request.form.get('password')):
            flash('Email ou senha inválidos', 'danger')
        else :
            login_user(user)
            return redirect(url_for('protected'))
    return render_template('login.html')

@app.route('/protected')
@login_required
def protected():
    flash('Olá {}, seja bem-vindo(a)'.format(current_user.username), 'success')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        CompleteFileName = generate(file.filename,
                                    request.form.get('campoforca'),
                                    request.form.get('modeloagua'),
                                    request.form.get('tipocaixa'),
                                    request.form.get('distanciacaixa'),
                                    request.form.get('neutralize'),
                                    request.form.get('double'),
                                    request.form.get('ignore'),
                                    current_user
                                    )  
        if request.form.get('download') == 'Baixar Lista de Comandos':
            return redirect(url_for('commandsdownload',
                    filename={"complete" : CompleteFileName,
                    "name": file.filename.split('.')[0]}))
        if request.form.get('execute') == 'Executar':
            file = request.files.get('file')
            moleculename = file.filename.split('.')[0]
            if upload_file(file, current_user.username, moleculename):
                AbsFileName = os.path.join(Config.UPLOAD_FOLDER,
                        current_user.username, moleculename , 'run',
                        'logs/', file.filename)
                execute(AbsFileName, CompleteFileName, current_user.username, moleculename)
            #3 - redirecionar para pagina de espera
            #na pagina deve ser possivel cancelar o processamento
            #deve ser adicionado a classe user se o mesma esta ou
            #não com processo em andamento
            else:
                flash('Extensão do arquivo está incorreta', 'danger')
    return render_template('index.html')

@login_required
@app.route('/download/<filename>')
def commandsdownload(filename):
    filename = ast.literal_eval(filename)
    return send_file('{}{}/{}/{}'.format(Config.UPLOAD_FOLDER,
            current_user.username,filename["name"],filename["complete"]), as_attachment=True)

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Por favor, faça Login', 'warning')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
