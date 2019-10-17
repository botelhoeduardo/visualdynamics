from .config import Config
from .execute import create_log 

def Date_finish():
    directory = Config.UPLOAD_FOLDER+"executing"
    archive = open(directory, "r")
    f = archive.readlines()
    for i, text in enumerate(f):
        if text.find('/') > -1:
            f = f[i].split('/VDfiles/')
            f = f[1].split(' \n')
            directory = Config.UPLOAD_FOLDER+f[0]
            archive = open(directory, "r")
            f = archive.readlines()
            last_line = f[len(f)-1]
            last_line = last_line.split('\n')
            date = last_line[0].split(',')
            for i, text in enumerate(date):
                if text.find('will finish') > -1:
                    date_finish = date[i]
                    return date_finish
    archive.close()         
    date_finish = 'Carregando data final da dinâmica...'
    return date_finish                
