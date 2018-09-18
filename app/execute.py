from .config import Config
from datetime import datetime
import subprocess, os, sys

def execute(LogFileName, CommandsFileName):
    LogFile = create_log(LogFileName)
    
    result = subprocess.check_output(['ls', '-l']).decode(sys.stdout.encoding)

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
