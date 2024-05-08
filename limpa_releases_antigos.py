import sys
import os
from datetime import datetime, timedelta

path_releases_comandos = "/home/pi/cm_releases_git"
path_releases = "/home/pi/mini-pc-upload-github-infra-compiled/releases/"

now_legacy = (datetime.utcnow() - timedelta(days=2)).strftime("%y%m%d")
arrfiles = os.listdir(path_releases_comandos)

for files in arrfiles:
    comandos = []
    full_path = path_releases_comandos + "/" + files
    prefixo = files[0:6]
    release = files[0:12]
    
    if prefixo <= now_legacy:
        comandos.append("sudo rm -rf " + full_path)

        full_path = path_releases + "/" + release
        comandos.append("sudo rm -rf " + full_path)
        
    for comando in comandos:
        try:
            os.system(comando)
        except:
            pass

