from app import app, login_manager
from flask import render_template, request, redirect, url_for, flash, send_file
from app.models import User
from flask_login import logout_user, login_required, login_user, current_user
from app.config import os, Config
from app.generate import generate

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
        if request.form.get('execute') == 'Baixar Lista de Comandos':
            CompleteFileName = generate(request.form.get('file'),
                                        request.form.get('campoforca'),
                                        request.form.get('modeloagua'),
                                        request.form.get('tipocaixa'),
                                        request.form.get('distanciacaixa'),
                                        request.form.get('neutralize'),
                                        request.form.get('double'),
                                        request.form.get('ignore'),
                                        current_user
                                        )            
            return redirect(url_for('commandsdownload', filename=CompleteFileName))
    return render_template('index.html')

@login_required
@app.route('/download/<filename>/')
def commandsdownload(filename):
    return send_file('{}{}/{}'.format(Config.UPLOAD_FOLDER, current_user.username,filename), as_attachment=True)

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
