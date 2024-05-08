import sys
import os
import paramiko
from time import sleep
import time
from datetime import datetime
import funcoes
import threading
import math

def append_file(arquivo, linha):
    linha = str(datetime.utcnow()) + " - " + linha

    with open(arquivo, "a") as fil:
        fil.write(linha + "\n")
    fil.close()

def executaComandoSSH(cliente, com_exec):
    saidaArr = []
    stdin, stdout, stderr = cliente.exec_command(com_exec)
    saida = stdout.read().decode("utf-8")
    erro = stdout.channel.recv_exit_status()
    stdin.flush()
    stdin.close()
    saidaArr.append(erro)
    saidaArr.append(saida)

    return saidaArr

path_maquinas_check = "/home/pi/mini-pc-upload-github-infra-compiled/"
path = "/home/pi/mini-pc-upload-github-infra-compiled/"

server = '177.71.253.58'
conta_shellhub = 'buspaycxshellhub'
user_so = 'pi'
pwd_so = 'Bus7@tyH5g'

release = ""
try:
    file_maquinas = path_maquinas_check + "/lista_maquinas/maquinas_ips.txt"
    path_relatorio = path_maquinas_check + "/relatorio_alcance/"
    file_relatorio = path_relatorio + "/relatorio.txt"	
    file_detalhes_veiculos = path_maquinas_check + "/infos_maquinas/instalacao_por_maquina.txt"

    os.system("sudo mkdir -p " + path_relatorio)
    os.system("sudo rm -rf " + path_relatorio + "/*")
    os.system("sudo touch " + file_relatorio)
except Exception as e:
    pass

# Comecamos a ler a lista de maquinas para esta execucao
with open(file_maquinas) as fil:
    lines = fil.readlines()
    lines = [line.strip() for line in lines]
    maquinas = lines
    del lines

def thread_por_maquina(maquina,i):
    maquina = maquina.strip()

    print("Acessando maquina " + maquina)

    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    string_connect = user_so + "@" + conta_shellhub + "." + maquina

    # Primeiro, checamos se a maquina tem um IP
    ip = funcoes.obtem_ip_maquina(maquina)

    if ip != "":
        string_connect = user_so
        server_connect = ip
    else:
        server_connect = server
        string_connect = user_so + "@" + conta_shellhub + "." + maquina

    try:
        cliente.connect(server_connect, username=string_connect, password=pwd_so, look_for_keys=False, timeout=5)

        stdin, stdout, stderr = cliente.exec_command("whoami", timeout=2)
        saida = stdout.read().decode("utf-8")
        erro = stdout.channel.recv_exit_status()
        stdin.flush()
        stdin.close()

        if erro < 0:
            conectado = False
        else:
            conectado = True
    except Exception as e:
        conectado = False

    if not conectado:
        append_file(file_relatorio, maquina + "|Sem conexao|")
        return
    else:
        pega_log = False
        
        string_saida = ""

        # Primeiro, checamos se ja foi executado
        arrSaida = executaComandoSSH(cliente, "sudo ls -l /home/pi/caixa-magica-operacao/aberto.txt")
        if len(arrSaida[1]) > 0:
            string_saida = maquina + "|Viagem aberta|"
        else:
            string_saida = maquina + "|Viagem fechada|"
        
        # Obtemos infos do veiculo em questao
        try:
            with open(file_detalhes_veiculos) as fil:
                lines = fil.readlines()
                lines = [line.strip() for line in lines]
                
                for registro in lines:
                    colunas = registro.split("|")
                    
                    if str(maquina) == str(colunas[0]):
                        string_saida = string_saida + "Onibus: " + str(colunas[4]) + "|Operadora: " + str(colunas[1]) + "|Versao: " + str(colunas[7]) + "|IP: " + str(colunas[8])
                        break
        except Exception as e:
            print(str(e))
            pass

        append_file(file_relatorio, string_saida)
    try:
        cliente.close()
        del cliente
    except:
        pass

os.system("clear")

# Roda script para obter detalhes dos veiculos
os.system("sudo python3 obtem_infos_onibus.py") 

tamanho = math.ceil(len(maquinas) / 50)
ret = (funcoes.chunkify(maquinas, tamanho))

print("Iniciando, aguarde...")
threads = []
i = 0

for registro in ret:
    maquinas = registro

    for maquina in maquinas:
        arrMaq = maquina.split("|")
        maquina = arrMaq[0]
        t = threading.Thread(target=thread_por_maquina, args=(maquina,i))
        t.start()
        threads.append(t)
        i = i +1

    for thread in threads:
        thread.join(60)

print("Gerando relatorio, aguarde...")
sleep(1)

# Exibindo relatorio
with open(file_relatorio) as fil:
    lines = fil.readlines()
    lines = [line.strip() for line in lines]
    os.system("clear")
    print("Relatorio execucao:")
    for line in lines:
        print(line)
