from .config import Config
import subprocess, os

def execute(filename):
    print(filename)
    result = subprocess.check_output(['ls', '-l'])
    #print(result)