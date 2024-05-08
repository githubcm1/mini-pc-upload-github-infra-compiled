import os
import sys
import paramiko
from datetime import datetime, timedelta
from time import sleep
import funcoes
import threading
import math
import subprocess
import atualiza_variaveis

release = ""
path = "/home/pi/mini-pc-upload-github-infra-compiled"
path_release=""
file_maquinas =""
file_em_exec = path + "/release_em_exec.txt"
path_script_vars = path + "/scripts_vars_validadores/"

server = '177.71.253.58'
conta_shellhub = 'buspaycxshellhub'
user_so = 'pi'
pwd_so = 'Bus7@tyH5g'

#user_so = 'buspay'
#pwd_so = '@buspay'

path_token = path + '/obtem_token.py'
output = subprocess.getoutput("sudo python3 "+path_token)
token = output.strip()

header = "\033[36m############################################ RELEASE DISPARADA ########################################\033[97m\n\n"

def append_file(arquivo, linha):
    linha = str(datetime.utcnow()) + " - " + linha
    
    with open(arquivo, "a") as fil:
        fil.write(linha + "\n")
    fil.close()

def isRaspberry(cliente):
    com_exec = "sudo cat /proc/cpuinfo"
    stdin, stdout, stderr = cliente.exec_command(com_exec)
    saida = stdout.read().decode("utf-8")
    erro = stdout.channel.recv_exit_status()
    stdin.flush()
    stdin.close()

    saida = saida.replace("\n", "").lower()

    if 'raspberry' in saida:
        return True

    return False


def check_viagem_aberta(cliente):
    com_exec = "ls -l cat /home/pi/caixa-magica-operacao/aberto.txt"
    stdin, stdout, stderr = cliente.exec_command(com_exec)
    saida = stdout.read().decode("utf-8")
    erro = stdout.channel.recv_exit_status()
    stdin.flush()
    stdin.close()

    if erro < 0:
        return False

    if saida == None or saida == "":
        return False
    return True

def check_same_version(cliente, versao):    
    com_exec = "cat /home/pi/caixa-magica/version.txt"
    stdin, stdout, stderr = cliente.exec_command(com_exec)
    saida = stdout.read().decode("utf-8")
    erro = stdout.channel.recv_exit_status()
    stdin.flush()
    stdin.close()
    saida = saida.replace("\n","").strip()

    if versao.strip() == saida:
        return True
    return False


def check_crontab_agendada(cliente, release):
    try:
        com_exec = "sudo crontab -l"
        stdin, stdout, stderr = cliente.exec_command(com_exec)
        saida = stdout.read().decode("utf-8")
        erro = stdout.channel.recv_exit_status()
        stdin.flush()
        stdin.close()

        if erro < 0:
            return False

        # Se nao ha nada no crontab
        if len(saida) <= 0:
            return False
        # Caso tenha algo no crontab
        else:
            if 'releases_cm/'+str(release) in saida:
                return True
            return False

            # Se tem alguma crontab com o ID da release, entao houve agendamento
            #if release in saida:
            #    if "MIN HORA DIA MES" in saida:
            #        return False
            #    else:
            #        return True
    except:
        pass

    return False

def check_ja_atualizada(cliente):
    try:
        com_exec = "ls -l /home/pi/releases_cm/" + release + "/executado.txt"
        stdin, stdout, stderr = cliente.exec_command(com_exec)
        saida = stdout.read().decode("utf-8")
        erro = stdout.channel.recv_exit_status()
        stdin.flush()
        stdin.close()
    
        if erro < 0:
            return False
        
        if len(saida) <= 0:
            return False
        return True
    except:
        return False


def obtem_ip_maquina(maquina):
    return funcoes.obtem_ip_maquina(maquina)

def executaSSH(maquina, contador_thread, versao_git):
    sleep(0.5)

    if not os.path.exists(path_script_vars):
        os.makedirs(path_script_vars)

    arq_log = path_sucesso + "/" + maquina + ".txt"
    if os.path.exists(arq_log):
        print(maquina + ": Ja atualizada")
        return

    print(str(datetime.utcnow()) + " - Conectando em " + maquina)
    cnt = 0
    limite = 3
    limite_com_exec = 3
    sucesso = True

    arq_log = path_logs + "/" + maquina + ".txt"
    arq_log_erros = path_erros + "/" + maquina + ".txt"
    os.system("sudo rm -f " + arq_log)
    os.system("sudo touch " + arq_log)

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

            #print(server_connect + " " + string_connect + " " + pwd_so)

            try:
                cliente.connect(server_connect,22, username=string_connect, password=pwd_so, look_for_keys=False)
                conectado = True
            except:
                conectado = False

            #print(str(conectado) + " " + server_connect) 

            if not conectado:
                append_file(arq_log, "Nao conectado. Efetuando nova tentativa")
                cnt = cnt + 1
                sleep(0.5)
            else:
                hardware_raspberry = isRaspberry(cliente)
                if hardware_raspberry:
                    string_ret = "Maquina nao pode ser uma Raspberry. Atualizacao impossibilitada por este atualizador."
                    print(string_ret)
                    append_file(arq_log_erros, string_ret)
                    return    

                append_file(arq_log, "Conectado. Iniciando gravacao dos comandos")
                comandos = []
                comandos_cron = []
                comandos.append("whoami")
                comandos.append("sudo rm -rf " + path_exec_destino)
                comandos.append("sudo mkdir -p " + path_exec_destino)
                comandos.append("sudo rm -rf " + path_exec_destino + "/releases_comandos/")

                # Para comando da lista, colocamos dentro do arquivo de execucao no destino
                # TODO: AO INVES DE RODAR ESTES COMANDOS, BAIXAR A LISTA ORIUNDA DO GITHUB (releases-comandos
                comando = "sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-releases-comandos.git " + path_exec_destino + "/releases_comandos/"
                comandos.append(comando)
                comando = "sudo cp " + path_exec_destino + "/releases_comandos/" + release + "_comandos.txt " + path_exec_destino + "/executa.sh"
                comandos.append(comando)

                dir_temp_rem = '/home/'+user_so+'/temp/'
                comando = 'mkdir -p '+dir_temp_rem
                comandos.append(comando)

                # Pegamos aqui os valores das variaveis
                arquivo_vars_validador = atualiza_variaveis.gera_arq_troca_vars(maquina, release)

                # Transfere o arquivo via ftp
                ftp = cliente.open_sftp()
                num_tries_ftp = 0

                while num_tries_ftp < 5:
                    try:
                        ftp.put(arquivo_vars_validador,dir_temp_rem+os.path.basename(arquivo_vars_validador))
                        num_tries_ftp = 9999
                    except Exception as e:
                        print(str(e))
                        num_tries_ftp = num_tries_ftp+1

                # Move o arquivo do diretorio temp para o diretorio destino
                comando = 'sudo mv '+dir_temp_rem + os.path.basename(arquivo_vars_validador) + ' ' + path_exec_destino
                comandos.append(comando)
                comando = 'sudo chown root:root '+dir_temp_rem + os.path.basename(arquivo_vars_validador)
                comandos.append(comando)

                comando_vars = 'sudo sh '+os.path.basename(arquivo_vars_validador)
                comandos.append("sudo sed -i 's/SCRIPT_VARS/"+comando_vars+"/g' "+ path_exec_destino+"/executa.sh")

                comando = "sudo cp " + path_exec_destino + "/releases_comandos/" + release + "_agenda_cron.sh " + path_exec_destino + "/agenda_cron.sh"
                comandos.append(comando)

                # Agenda a cron para ser executada
                comandos.append("sudo sh " + path_exec_destino + "/agenda_cron.sh")

                # Acerca do horario de agendamento, pegamos - na maquina cliente - o horario atual e utilizamos-o como referencia
                # para o agendamento
                comando = 'date +"%Y-%m-%d %H:%M:%S"'
                stdin, stdout, stderr = cliente.exec_command(comando)
                saida = stdout.read().decode("utf-8").strip()
                now = datetime.strptime(saida, '%Y-%m-%d %H:%M:%S')
                

                # Considera o horario tradicional
                now = now + timedelta(minutes=3)
                DIA_EXEC = now.strftime("%d")
                MES_EXEC = now.strftime("%m")
                HORA_EXEC = now.strftime("%H")
                MIN_EXEC = now.strftime("%M")

                comandos.append("sudo sed -i 's/MIN/" + str(MIN_EXEC) +"/' " + path_exec_destino + "/agenda_cron.sh")
                comandos.append("sudo sed -i 's/HORA/" + str(HORA_EXEC) +"/' " + path_exec_destino + "/agenda_cron.sh")                
                comandos.append("sudo sed -i 's/DIA/" + str(DIA_EXEC) +"/' " + path_exec_destino + "/agenda_cron.sh")
                comandos.append("sudo sed -i 's/MES/" + str(MES_EXEC) +"/' " + path_exec_destino + "/agenda_cron.sh")

                comandos.append("sudo rm -rf " + path_exec_destino + "/releases_comandos/")

                # Agora, agendamos a execucao no destino
                comandos.append("sudo sh " + path_exec_destino + "/agenda_cron.sh")

                comandos.append("sudo pkill -9 -f executa.sh")

                #comandos = []
                #comandos.append("sudo touch " + path_exec_destino + "/" + str(contador_thread) + ".txt")

                cnt_comandos = 0
                erro_exec_primeira = False

                if not ignorar_viagem_aberta:
                    viagem_aberta = check_viagem_aberta(cliente)
                    if viagem_aberta:
                        print("Viagem aberta. Atualizacao impossibilitada neste momento")
                        append_file(arq_log_erros, "Viagem aberta. Atualizacao impossibilitada")
                        return

                # Checa se ja foi atualziada
                ja_atualizada = check_ja_atualizada(cliente)
                if ja_atualizada:
                    print(maquina + ": Ja atualizada")
                    return

                # Se for a mesma versao, tambem indicamos que ja foi atualizada
                if check_same_version(cliente, versao_git):
                    print(maquina + ": Ja atualizada (mesma versao "+versao_git+")")
                    return

                # Checa se o processo esta agendado aguardando ou em execucao
                crontab_agendada = check_crontab_agendada(cliente, release)
                if crontab_agendada:
                    print(maquina + ": Ja agendada")
                    return

                for com_exec in comandos:
                    if erro_exec_primeira:
                        append_file(arq_log_erros, "Conexao falhou")
                        return

                    num_tries_com_exec = 0
                    erro = 1

                    while num_tries_com_exec < limite_com_exec:
                        append_file(arq_log, "Rodando comando " + com_exec)
                        stdin, stdout, stderr = cliente.exec_command(com_exec)
                        saida = stdout.read().decode("utf-8")
                        erro = stdout.channel.recv_exit_status()
                        append_file(arq_log, "Saida comando " + com_exec + ": " + saida)
                        #print("Saida comando " + com_exec + ": " + saida + " " + str(stdout) )
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
            
                # Se chegou aqui, eh porque houve sucesso na execucao de todos os comandos
                if sucesso:
                    arq_log_agendado = path_agendados + "/" + maquina + ".txt"
                    os.system("sudo rm -f " + arq_log_agendado)
                    os.system("sudo touch " + arq_log_agendado)

        except Exception as e:
            append_file(arq_log, "Nao conectado: " + str(e))
            cnt = cnt+1

            if cnt == limite:
                arq_log_erros = path_erros + "/" + maquina + ".txt"
                os.system("sudo rm -f " + arq_log_erros)
                os.system("sudo touch " + arq_log_erros)

release = ''
try:
    release = sys.argv[1]
except:
    try:
        with open(path + "/ultimo_release.txt", "r") as f:
            release = f.read()
        f.close()
    except:
        pass

if release == '':
    print("release nao informado")
    quit()


# Pegamos a versao do fonte do GIT
try:
    path_aux_versao = '/home/pi/cm_releases_git/'+release+'_version.txt'
    with open(path_aux_versao) as f:
        versao_git = f.read().strip()
    f.close()
except:
    versao_git = ''

if versao_git == '':
    print("Sem versao da aplicacao no GIT.")
    quit()

while 1:
    try:
        # Atualizamos o arquivo de release em execucao
        with open(path + "/ultimo_release.txt", "w") as f:
            f.write(str(release).strip())
        f.close()

        sleep(2)

        os.system("clear")
        print(header)
        print("EXECUCAO RELEASE ID "+str(release) +": "+str(datetime.now()))
        ignorar_viagem_aberta = False
        for row in sys.argv:
            if row== "ignorar_viagem_aberta=yes":
                ignorar_viagem_aberta = True
                break

        try:
            path_release = path + "/releases/" + release

            # Checa se a release existe
            if not os.path.exists(path_release):
                print("Release " + release + " nao existe.")
                quit()

            file_maquinas = path_release + "/lista_maquinas/maquinas.txt"

            file_comandos = path_release + "/lista_comandos/comandos.txt"
            path_erros= path_release + "/logs_por_maquina_erros/"
            path_sucesso= path_release +"/logs_por_maquina_sucesso/"
            path_logs = path_release + "/logs_por_maquina/"
            path_agendados = path_release + "/logs_maquinas_agendadas/"

            os.system("sudo mkdir -p " + path_logs)
            os.system("sudo mkdir -p " + path_sucesso)
            os.system("sudo mkdir -p " + path_erros)
            os.system("sudo mkdir -p " + path_agendados)

            path_exec_destino = "/home/pi/releases_cm/" + release + "/"
            file_exec_destino = path_exec_destino + "/executa.sh"

            # Se chegou ate aqui, entao devemos reiniciar a release
            os.system("sudo rm -rf " + path_erros + "/*")

        except Exception as e:
            print(str(e))
            pass

        if release == "":
            print("Release nao informado")
            quit()

        try:
            if sys.argv[2] == 'force':
                os.system("sudo rm -f " + file_em_exec)
        except:
            pass

        if os.path.exists(file_em_exec):
            print("Ja existe um release em execucao. Aguarde")
            quit()


        # Checamos aqui se o numero de maquinas ultrapassa o limite permitido da re$
        atingiu_limite_maquinas = funcoes.check_excesso_maquinas_release(release)

        if atingiu_limite_maquinas:
            print("Release " + str(release) + " esta com um numero de maquinas maior do que o permitido.\n\nRevise a lista e gere um novo release.")
            quit()

        # Comecamos a ler a lista de maquinas para esta execucao
        with open(file_maquinas) as fil:
            lines = fil.readlines()
            lines = [line.strip() for line in lines]
            maquinas = lines
            del lines
        fil.close()

        # Abrimos o arquivo de comandos
        with open(file_comandos) as fil:
            lines = fil.readlines()
            lines = [line.strip() for line in lines]
            comandos = lines
            del lines
        fil.close()

        # Grava arquivo que indica que ja ha um release em execucao
        os.system("sudo touch " + file_em_exec)
        os.system("sudo echo '" + release + "' | sudo tee " + file_em_exec)

        tamanho = math.ceil(len(maquinas) / 20)
        ret = (funcoes.chunkify(maquinas, tamanho))

        print("Iniciando, aguarde...")
        threads = []
        i = 0

        for registro in ret:
            maquinas = registro

            for maquina in maquinas:
                t = threading.Thread(target=executaSSH, args=(maquina, i, versao_git))
                t.start()
                threads.append(t)
                i = i +1

            for thread in threads:
                thread.join(60)
            sleep(2)

        # Elimina arquivo de release em execucao
        os.system("sudo rm -f " + file_em_exec)

        print("Release " + release + " agendada nas maquinas especificadas.")
    except Exception as e:
        print(str(e))

    print("Proxima execucao em "+str( datetime.now()+timedelta(seconds=30) ))
    print("\nPressione CTRL + C para interromper a execucao a qualquer instante")
    sleep(30)
