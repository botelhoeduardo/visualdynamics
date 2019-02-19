from .config import Config, os

def CheckUserDynamics(username):
    '''
    Return True if the executing dynamic belongs to the logged user
    '''
    fname = Config.UPLOAD_FOLDER + 'executing'
    if os.path.exists(fname):
        with open(fname,'r') as f:
            if f.readline() == username:
                return True
    return False