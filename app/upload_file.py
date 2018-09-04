from .config import Config
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def upload_file(file):
    filename = secure_filename(file)
    file.save(os.path.join(Config.PDB_FOLDER, filename))