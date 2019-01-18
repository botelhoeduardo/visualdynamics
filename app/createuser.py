from .models import User
from app import db

def createuser():
    confirma=False
    valid = ['y', 'Y', 'S', 's', 'N', 'n']

    while(confirma is False):
        username = input('Digite o nome do usuário:\n')
        email = input('Digite o email do usuário:\n')
        password = input('Digite a senha do usuário\n')

        resp = input('\nusername: {}\nemail: {}\nsenha: {}\n\nConfirma? (Y/n)'.format(
            username, email, password
        ))

        if resp not in valid:
            print('Opção Inválida:\n\n')
        elif resp is 'n' or resp is 'N':
            print('Digite Novamente:\n\n')
        else:
            print('Criando no banco de dados...\n')
            confirma=True
    
    u = User(username=username,email=email)
    u.set_password(password)

    db.session.add(u)
    db.session.commit()