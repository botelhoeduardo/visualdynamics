from .config import Config
from datetime import datetime
import subprocess, os, sys

def execute(LogFileName, CommandsFileName, username):
    LogFile = create_log(LogFileName) #cria o arquivo

    #abrir arquivo
    with open(CommandsFileName) as f:
        content = f.readlines()
    lines = [line.rstrip('\n') for line in content]

    #estabelecer o diretorio de trabalho
    os.chdir(Config.UPLOAD_FOLDER + username + '/PDBs/')

    command1 = lines[0].split(' ')

    try:
        result = subprocess.check_output(command1).decode(sys.stdout.encoding)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))



    write_log(LogFile, result)
    close_log(LogFile)


def create_log(LogFileName):
    #formatando nome do arquivo log
    LogFileName = LogFileName.split('.')
    LogFileName.pop()
    LogFileName = ".".join(LogFileName) + \
            " - {}-{}-{} [{}:{}:{}]{}".format(
            datetime.now().year, datetime.now().month,
            datetime.now().day, datetime.now().hour,
            datetime.now().minute, datetime.now().second,
            '.log.txt'
            )
    
    LogFile = open(LogFileName, "w+")
    return LogFile

def write_log(LogFile, message):
    LogFile.write(message)

def close_log(LogFile):
    LogFile.close()
