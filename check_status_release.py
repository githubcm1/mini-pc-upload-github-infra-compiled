import sys
import os
import paramiko
from time import sleep
import time
from datetime import datetime, timedelta
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

path_maquinas_check = "/home/pi/mini-pc-upload-github-infra-compiled/releases/"
path = "/home/pi/mini-pc-upload-github-infra-compiled/"

server = '177.71.253.58'
conta_shellhub = 'buspaycxshellhub'
user_so = 'pi'
pwd_so = 'Bus7@tyH5g'

try:
    release = ''
    try:
        release = sys.argv[1]
    except:
        try:
            with open(path + "/ultimo_release.txt", "r") as f:
                release = f.read()
                print(release)
            f.close()
        except:
            pass

    file_maquinas = path_maquinas_check + "/" + release + "/lista_maquinas/maquinas.txt"
    path_log_maquinas = path_maquinas_check + "/" + release + "/logs_por_maquina/"
    path_maquinas_check = path_maquinas_check + "/" + release + "/logs_maquinas_agendadas/"
    path_maquinas_sucesso = path_maquinas_check + "/../logs_por_maquina_sucesso/"
    path_maquinas_erros = path_maquinas_check + "/../logs_por_maquina_erros/"
    path_maquinas_pendentes = path_maquinas_check + "/../logs_por_maquina_pendentes/"
    path_relatorio = path_maquinas_check + "/../relatorio_atualizacao/"
    file_relatorio = path_relatorio + "/relatorio.txt"	

    # Limpa os diretorios, para reiniciar o check
#    os.system("sudo rm -rf " + path_maquinas_sucesso + "/*")
#    os.system("sudo rm -rf " + path_maquinas_erros + "/*")
except Exception as e:
    print(str(e))
    pass


if release == "":
    print("Informe o release para conferencia")
    quit()

# Pegamos a lista de maquinas agendadas
#maquinas = [f for f in os.listdir(path_maquinas_check) if os.path.isfile(os.path.join(path_maquinas_check,f))]

# Comecamos a ler a lista de maquinas para esta execucao
with open(file_maquinas) as fil:
    lines = fil.readlines()
    lines = [line.strip() for line in lines]
    maquinas = lines
    del lines

def thread_por_maquina(maquina,i):
    maquina = maquina.strip()

    print("Acessando maquina " + maquina)

    file_maquina_sucesso = path_maquinas_sucesso + "/" + maquina + ".txt"
    file_maquina_erro = path_maquinas_erros + "/" + maquina + ".txt"
    file_maquina_pendente = path_maquinas_pendentes + "/" + maquina + ".txt"

    if os.path.exists(file_maquina_sucesso):
        append_file(file_relatorio, maquina + " - Atualizada")
        os.system("sudo rm -f " + file_maquina_erro)

        return

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
        print(str(e))
        conectado = False

    if not conectado:
        os.system("sudo touch " + file_maquina_pendente)
        append_file(file_relatorio, maquina + " - Pendente, sem conexao")
        return
    else:
        pega_log = False
        file_log_cliente = "/home/pi/releases_cm/" + release + "/logs_executa.txt"

        # Primeiro, checamos se ja foi executado
        arrSaida = executaComandoSSH(cliente, "ls -l /home/pi/releases_cm/" + release + "/executado.txt")
        if len(arrSaida[1]) > 0:
            append_file(file_relatorio, maquina + " - Atualizada")
            os.system("sudo touch " + file_maquina_sucesso)
            os.system("sudo rm -f " + file_maquina_erro)
            pega_log = True
        else:
            # Checa se tem viagem aberta
            arrSaida = executaComandoSSH(cliente, "sudo ls -l /home/pi/caixa-magica-operacao/aberto.txt")
            if len(arrSaida[1]) > 0:
                append_file(file_relatorio, maquina + " - NOTA: Sem atualizacao, ha viagem aberta na maquina")
            
            arrSaida = executaComandoSSH(cliente, "sudo crontab -l")
            # Se nao tem retorno, entao deu erro
            if not release in arrSaida[1]:
                append_file(file_relatorio, maquina + " - Erro, crontab nao agendada")
                os.system("sudo touch " + file_maquina_erro)
            else:
                # Checamos se o processo ainda esta em execucao
                arrSaida = executaComandoSSH(cliente, "sudo tail -n1 " + file_log_cliente)
                
                # Se tem log, entao o processo esta em exec
                if len(arrSaida[1]) > 0:
                    append_file(file_relatorio, maquina + " - Pendente, crontab em execucao")
                    pega_log = True

                    file_log_por_maquina = path_log_maquinas + "/" + maquina + "_log_cliente.txt"
                else:
                    append_file(file_relatorio, maquina + " - Pendente, crontab agendada")
                os.system("sudo touch " + file_maquina_pendente)
                os.system("sudo rm -f " + file_maquina_erro)
        
        file_log_por_maquina = path_log_maquinas + "/" + maquina + "_log_cliente.txt"
        os.system("sudo rm -f " + file_log_por_maquina)
        if pega_log:
            arrSaida = executaComandoSSH(cliente, "sudo cat " + file_log_cliente)
            if arrSaida[0] == 0:
                with open(file_log_por_maquina,"w") as fil:
                    fil.write(arrSaida[1].strip())
                    fil.close()
    try:
        cliente.close()
        del cliente
    except:
        pass

while 1:
    os.system("clear")
    sleep(0.5)

    header = """\033[31m############################################ RELATORIO RELEASE - ATUALIZACAO VALIDADORES ######################################\033[97m
             """
    header = header.strip() + "\n\n"
    print(header)

    print("EXECUCAO RELEASE ID "+str(release)+" EM "+str(datetime.now()))

    os.system("sudo mkdir -p " + path_maquinas_sucesso)
    os.system("sudo mkdir -p " + path_maquinas_erros)
    os.system("sudo mkdir -p " + path_maquinas_pendentes)
    os.system("sudo mkdir -p " + path_relatorio)
    os.system("sudo rm -rf " + path_relatorio + "/*")
    os.system("sudo touch " + file_relatorio)

    tamanho = math.ceil(len(maquinas) / 50)
    ret = (funcoes.chunkify(maquinas, tamanho))

    print("Iniciando, aguarde...")
    threads = []
    i = 0

    for registro in ret:
        maquinas = registro

        for maquina in maquinas:
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
        print(header)
        print("EXECUCAO RELEASE ID "+str(release)+" EM "+str(datetime.now()))
        print("Relatorio execucao:")
        for line in lines:
            print(line)

    print("\n\n\n")
    print("Aguardando nova atualização em "+str(datetime.now()+timedelta(minutes=1))+"..." )
    print("Pressione CTRL + C para interromper a qualquer instante.")
    sleep(60)
