import sys
import os
import paramiko
from time import sleep
import time
from datetime import datetime
import funcoes
import threading
import math
import json

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
    path_relatorio = path_maquinas_check + "/infos_maquinas/"
    file_maquinas = path_maquinas_check + "/lista_maquinas/maquinas_ips.txt"
    path_relatorio_por_maquina = path_relatorio + "/por_maquina/"
    file_relatorio = path_relatorio + "/instalacao_por_maquina.txt"

    os.system("sudo mkdir -p " + path_relatorio) 
    os.system("sudo mkdir -p " + path_relatorio_por_maquina)

    # Exclui o arquivo de maquinas
    os.system("sudo rm -rf " + file_relatorio)

    # Regera o arquivo, colocando um cabecalho no mesmo
    cabecalho = "serial|operadoraid|caixamagicaid|onibusid|numeroveiculo|bilhetadoraid|codigoacesso|version" + "\n"

    with open(file_relatorio, "w") as fil:
        fil.write(cabecalho)
        fil.close()
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

    file_maquina = path_relatorio_por_maquina + "/" + maquina + "_instalacao.json"
    file_maquina_version = path_relatorio_por_maquina + "/" + maquina + "_version.txt"

    if conectado:
        pega_log = False

        # Primeiro, checamos se ja foi executado
        arrSaida = executaComandoSSH(cliente, "sudo cat /home/pi/caixa-magica-operacao/instalacao.json")
        if len(arrSaida[1]) > 0:
            # Grava saida no arquivo da maquina
            with open(file_maquina, "w") as fil:
                fil.write(arrSaida[1])
                fil.close()

        # Procura obter tambem a versao que esta
        arrSaida = executaComandoSSH(cliente, "sudo cat /home/pi/caixa-magica/version.txt")
        if len(arrSaida[1]) > 0:
            # Grava saida no arquivo da maquina
            with open(file_maquina_version, "w") as fil:
                fil.write(arrSaida[1])
                fil.close()

    # Abre o arquivo para extracao de infos
    try:
        with open(file_maquina) as json_data:
            aux = json.load(json_data)
            registro = maquina + "|" + str(aux['operadora']) + "|" + str(aux['caixa_id']) + "|" + str(aux['veiculo']) + "|" + str(aux['numeroVeiculo']) + "|" + str(aux['bilhetadoraId']) + "|" + str(aux['acesso']) 
    except:
        registro = maquina + "|" + "" + "|" + "" + "|" + "" + "|" + "" + "|" + "" + "|" + ""

    # Abre o arquivo para extracao de infos
    try:
        with open(file_maquina_version) as fil:
            aux = fil.readline()
            registro = registro + "|" + aux 
    except:
        registro = registro + "|Versao nao encontrada"

    # Adiciona o IP
    try:
        registro = registro + "|" + ip
    except:
        registro = registro + "|sem IP"

    registro = registro + "\n"

    with open(file_relatorio, "a") as fil:
        fil.write(registro)
        fil.close()
        
    try:
        cliente.close()
        del cliente
    except:
        pass

os.system("clear")
print("Obtendo infos de instalacao dos veiculos cadastrados")

tamanho = math.ceil(len(maquinas) / 100)
ret = (funcoes.chunkify(maquinas, tamanho))

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

