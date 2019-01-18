from app import app, db
from app.models import User
from app.createuser import createuser

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'createuser':createuser}

