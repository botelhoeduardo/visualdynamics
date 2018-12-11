from .config import Config
from datetime import datetime
import subprocess, os, sys, shutil

def execute(LogFileName, CommandsFileName, username, filename):
    LogFile = create_log(LogFileName) #cria o arquivo log

    #transferir os arquivos mdp necessarios para a execução
    RunFolder = Config.UPLOAD_FOLDER + username + '/' + filename + '/run/'
    SecureMdpfilesFolder = os.path.expanduser('~') + '/visualdynamics/mdpfiles'
    MDPList = os.listdir(SecureMdpfilesFolder)
    for mdpfile in MDPList:
        fullmdpname = os.path.join(SecureMdpfilesFolder, mdpfile)
        if (os.path.isfile(fullmdpname)):
            shutil.copy(fullmdpname, RunFolder)

    #abrir arquivo
    with open(CommandsFileName) as f: #CODIGO PARA A PRODUÇÃO
    #with open('{}{}/{}/teste.txt'.format(Config.UPLOAD_FOLDER, username, filename)) as f: #Código para TESTE
        content = f.readlines()
    lines = [line.rstrip('\n') for line in content if line is not '\n']

    #estabelecer o diretorio de trabalho
    os.chdir(RunFolder)
    
    #comando para rodar o gromacs (resolve o erro gmx em containers)
    subprocess.Popen("source /usr/local/gromacs/bin/GMXRC", executable="/bin/bash", shell=True)

    try:
        for l in lines:
            l = l.split(' ')
            result = subprocess.check_output(l).decode(sys.stdout.encoding)
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
