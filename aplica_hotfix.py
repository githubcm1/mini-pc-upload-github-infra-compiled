import os
import sys
import paramiko
from datetime import datetime, timedelta
from time import sleep
import funcoes
import threading
import math

path = "/home/pi/mini-pc-upload-github-infra-compiled"
file_maquinas =""

server = '177.71.253.58'
conta_shellhub = 'buspaycxshellhub'
user_so = 'pi'
pwd_so = 'Bus7@tyH5g'

def obtem_ip_maquina(maquina):
    return funcoes.obtem_ip_maquina(maquina)

def executaSSH(maquina, contador_thread, comandos):
    sleep(0.5)

    print(str(datetime.utcnow()) + " - Conectando em " + maquina)
    cnt = 0
    limite = 3
    limite_com_exec = 3
    sucesso = True

    while cnt < limite:
        try:
            cliente = paramiko.SSHClient()
            cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Primeiro, checamos se a maquina tem um IP
            ip = obtem_ip_maquina(maquina) 

            if ip != "":
                string_connect = user_so
                server_connect = ip
            else:
                server_connect = server
                string_connect = user_so + "@" + conta_shellhub + "." + maquina

            try:
                cliente.connect(server_connect, username=string_connect, password=pwd_so, look_for_keys=False)
                conectado = True
            except:
                conectado = False

            if not conectado:
                print(maquina + " - Nao conectado. Efetuando nova tentativa")
                cnt = cnt + 1
                sleep(0.5)
            else:
                print(maquina + " - Conectado. Iniciando gravacao dos comandos")

                cnt_comandos = 0

                for com_exec in comandos:
                    com_exec = com_exec.strip()
                    print(com_exec)

                    if com_exec == "":
                        continue

                    print(maquina + " - Comando: " + com_exec)
                    num_tries_com_exec = 0
                    erro = 1

                    while num_tries_com_exec < limite_com_exec:
                        print(maquina + " - Rodando comando " + com_exec)
                        stdin, stdout, stderr = cliente.exec_command(com_exec)
                        saida = stdout.read().decode("utf-8")
                        erro = stdout.channel.recv_exit_status()
                        print(maquina + " - Saida comando " + com_exec + ": " + saida)
                        stdin.flush()
                        stdin.close()

                        if erro < 0 and cnt_comandos == 0:
                            num_tries_com_exec = limite_com_exec
                            erro_exec_primeira = True

                        if erro == 0:
                            num_tries_com_exec = limite_com_exec
                        else:
                            num_tries_com_exec = num_tries_com_exec+1
                            sleep(0.1)
                    
                    # Se a ultima tentativa de exec foi com erro
                    if erro < 0:
                        sucesso = False
                    else:
                        sucesso = True

                cnt = limite
                cliente.close()
                sleep(0.1)
                del cliente
        except Exception as e:
            print(str(e))
            print(maquina + " - Nao conectado: ")
            cnt = cnt+1

try:
    file_maquinas = path + "/lista_maquinas/maquinas_hotfix.txt"
    file_comandos = path + "/hotfix/comandos.txt"
except Exception as e:
    print(str(e))
    pass

# Comecamos a ler a lista de maquinas para esta execucao
with open(file_maquinas) as fil:
    lines = fil.readlines()
    lines = [line.strip() for line in lines]
    maquinas = lines
    del lines

# Abrimos o arquivo de comandos
with open(file_comandos) as fil:
    lines = fil.readlines()
    lines = [line.strip() for line in lines]
    comandos = lines
    del lines

tamanho = math.ceil(len(maquinas) / 20)
ret = (funcoes.chunkify(maquinas, tamanho))

print("Iniciando, aguarde...")
threads = []
i = 0

for registro in ret:
    maquinas = registro

    for maquina in maquinas:
        t = threading.Thread(target=executaSSH, args=(maquina, i, comandos))
        t.start()
        threads.append(t)
        i = i +1

    for thread in threads:
        thread.join(60)
    sleep(2)
