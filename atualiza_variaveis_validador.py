import os
import sys
import atualiza_variaveis as a
from time import sleep
from datetime import datetime

args=sys.argv
maquinas_atualizar = []
cnt = 0
while cnt < len(args):
    if cnt > 0:
        maquinas_atualizar.append(args[cnt])
    cnt=cnt+1

os.system("clear")
header = "\033[32m############################################ ATUALIZA PARAMETROS ########################################\033[97m\n\n"
print(header)

# Para cada maquina
for maquina in maquinas_atualizar:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Acessando "+maquina+ "...")
    try:
        a.troca_vars_arquivos(maquina, '', False)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Atualizada "+maquina+". Reboot da aplicação em execução")
    except Exception as e:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Erro "+maquina+": " + str(e))

    sleep(0.2)
