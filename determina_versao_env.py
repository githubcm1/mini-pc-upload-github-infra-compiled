import sys

path_atual = '/home/pi/mini-pc-src-caixa-magica/'
sys.path.insert(1, path_atual+ '/core/')
import endpoints

with open(path_atual + "/version.txt", "r") as f:
    version = f.read().strip()
    version = version.replace("_PROD", "")
    version = version.replace("_DEV", "")
    version = version.replace("_HOMOLOG", "")
    version = version + "_" + endpoints.getEnv()
    f.close()

with open(path_atual + "/version.txt", "w") as f:
    f.write(version)
    f.close()

