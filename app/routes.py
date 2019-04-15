from app import app, login_manager
from flask import render_template, request, redirect, url_for, flash, send_file, current_app
from .models import User
from flask_login import logout_user, login_required, login_user, current_user
from .config import os, Config
from .generate import generate
from .execute import execute
from .upload_file import upload_file
from .checkuserdynamics import CheckUserDynamics, CheckDynamicsSteps
from .admin_required import admin_required
import ast
import errno
import zipfile

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
            #check if the server is running
            try:
                f = open(Config.UPLOAD_FOLDER+'executing','x+')
                f.writelines('{}\n'.format(current_user.username))
                f.close()
                #os.path.exists(Config.UPLOAD_FOLDER + 'executing')
            except OSError as e:
                if e.errno == errno.EEXIST:
                    flash('O servidor está em execução', 'danger')
                    return redirect(url_for('index'))
            #preparação para executar
            MoleculeName = file.filename.split('.')[0]
            
            if upload_file(file, current_user.username):
                return redirect(url_for('executar', comp=CompleteFileName,
                    mol=MoleculeName, filename=file.filename))  
            else:
                flash('Extensão do arquivo está incorreta', 'danger')
    if CheckUserDynamics(current_user.username) == True:
        flash('','steps')    
        steplist = CheckDynamicsSteps(current_user.username)
        return render_template('index.html', actindex = 'active', steplist=steplist)
    return render_template('index.html', actindex = 'active')

@app.route('/executar/<comp>/<mol>/<filename>')
@login_required
def executar(comp,mol,filename):
    AbsFileName = os.path.join(Config.UPLOAD_FOLDER,
                    current_user.username, mol , 'run',
                    'logs/', filename)
    exc = execute(AbsFileName, comp, current_user.username, mol)
    flash('','steps')
    return redirect(url_for('index'))


@app.route('/ligante')
@login_required
def ligante():
    if CheckUserDynamics(current_user.username) == True:
        flash('','steps')   
    return render_template('ligante.html', actlig = 'active')

@app.route('/imgfiles')
@login_required
def imgsdownload():
    current_location = os.path.join(Config.UPLOAD_FOLDER, current_user.username)
    ziplocation = os.path.join(current_location, 'imagens.zip')
    
    zf = zipfile.ZipFile(ziplocation,'w')

    for folder, subfolders, files in os.walk(current_location):
 
        for file in files:
            if file.endswith('.PNG'):
                zf.write(os.path.join(folder, file), file, compress_type = zipfile.ZIP_DEFLATED)
    zf.close()

    return (send_file(ziplocation, as_attachment=True))


@app.route('/download/<filename>')
@login_required
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

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    UserData = User.query.all()
    return render_template('admin.html', UserData=UserData)
    if request.method == 'POST':
        user = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passconfirm = request.form.get('passwordconfirm')
        if password == passconfirm:
            new = User(username=user,email=email)
            new.set_password(password)
            db.session.add(new)
            db.session.commit()
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('index'))
        flash('Erro ao criar usuário', 'danger')
        return redirect(url_for('index'))

@app.route('/admin/<user>')
@admin_required
def edit_user(user):
    UserData = User.query.get(int(user))    return render_template('edit_user.html',UserData=UserData)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
