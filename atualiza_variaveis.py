import glob
import json
import os
import sys
import paramiko

path = "/home/pi/mini-pc-upload-github-infra-compiled"
path_script_vars = path + "/scripts_vars_validadores/"
path_ips = '/home/pi/mini-pc-upload-github-infra-compiled/lista_maquinas/maquinas_ips.txt'
username = 'pi'
pwd = 'Bus7@tyH5g'

path_vars = '/home/pi/mini-pc-upload-github-infra-compiled/variaveis/variaveis_validadores.txt'

with open(path_vars) as f:
    aux = f.readlines()
f.close()

arquivos_atualizar = []
for linha in aux:
    linha = linha.strip()
    if linha == '':
        continue
    colunas = linha.split("|")
    if colunas[1].strip() not in arquivos_atualizar:
        arquivos_atualizar.append(colunas[1].strip())

# Rotina usada para geracao do arquivo com variaveis
def gera_arq_troca_vars(maquina_serial, release=''):
    try:
        if not os.path.exists(path_script_vars):
            os.makedirs(path_script_vars)

        saida = troca_vars_arquivos(maquina_serial, release, True)
        nome_arq = path_script_vars + str(maquina_serial)+"_vars.sh"
        with open(nome_arq, "w") as f:
            f.write(saida)
        f.close()
        return nome_arq
    except Exception as e:
        pass

    return ''

# Rotina de atializacao dos arquivos
def troca_vars_arquivos(maquina_serial, release='', emite_saida=False):
    arquivos_atualizar_interno=[]

    # Se nao tem release, lemos da lista geral de arquivos
    if release == '':
        arquivos_atualizar_interno = arquivos_atualizar
    else:
        arquivos_atualizar_interno_aux = glob.glob('/home/pi/cm_releases_vars_git/'+release+'/*.json')
        for row in arquivos_atualizar_interno_aux:
            arquivos_atualizar_interno.append(os.path.basename(row))

    lenAux = len(arquivos_atualizar_interno)
    cnt = 0
    saida =''
    for arquivo in arquivos_atualizar_interno:
        cnt = cnt+1
        if cnt >= lenAux:
            reboot=True
        else:
            reboot = False

        aux =troca_vars_cliente(maquina_serial, release, arquivo, reboot, emite_saida)

        if emite_saida:
            saida = saida + aux

    return saida

def troca_vars_cliente(maquina_serial, release, arquivo, reboot=False, emite_saida=False):
    prefixo_dir = '/home/pi/caixa-magica-vars/'
    saida_txt=''
    path_json_saida_validador = prefixo_dir+""+arquivo

    try:
        # Abrimos o arquivo de variaveis, pegando todas que sejam do validador atual
        #path_vars = '/home/pi/mini-pc-upload-github-infra-compiled/variaveis/variaveis_validadores.txt'
        with open(path_vars) as f:
            aux=f.readlines()
        f.close()

        arrVars=[]
        for row in aux:
            row = str(row).split("|")
            if row[0] == maquina_serial and row[1] == arquivo:
                arrAux = []
                arrAux.append(row[2].replace("\n",""))
                arrAux.append(row[3].replace("\n",""))
                arrAux.append(row[4].replace("\n",""))
                arrVars.append(arrAux)
       
        ip = ''
        with open(path_ips) as f:
            lines = f.readlines()
        f.close()

        for linha in lines:
            arrAux = linha.split("|")
            if arrAux[0] == maquina_serial:
                ip = arrAux[1].replace("\n","")
                break

        # Se nao foi informado um release, devemos buscar o valor direto na maquina cliente
        if release == '':
            try:
                cliente = paramiko.SSHClient()
                cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                cliente.connect(ip, username=username, password=pwd, look_for_keys=False)
                conectado = True
            except:
                conectado = False
        else:
            conectado = True

        if conectado:
            if release == '':
                # Abrimos o arquivo remotamente
                path_json_saida = prefixo_dir+""+arquivo
                com_exec = "cat "+path_json_saida
                stdin, stdout, stderr = cliente.exec_command(com_exec)
                saida = stdout.read().decode("utf-8")
                erro = stdout.channel.recv_exit_status()
                stdin.flush()
                stdin.close()
                saida = saida.replace("\n","").strip()
                json_arq = json.loads(saida)
            else:
                path_json_saida = '/home/pi/cm_releases_vars_git/'+release+'/'+arquivo
                with open(path_json_saida) as f:
                    json_arq = json.load(f)
                f.close()

            for chave in json_arq:
                for vars_maquina in arrVars:
                    if vars_maquina[0].strip() == chave.strip():
                        tipo_dado = vars_maquina[1].strip()
                        valor = vars_maquina[2]

                        if tipo_dado == 'float':
                            valor = float(valor)
                        elif tipo_dado == 'str':
                            valor = str(valor)
                        elif tipo_dado == 'bool':
                            valor = bool(valor)
                        elif tipo_dado == 'int':
                            valor = int(valor)
                        else:
                            valor = str(valor)
                        json_arq[chave] = valor
                       
                        break
                    else:
                        try:
                            subkeys = json_arq[chave].keys()
                            
                            for subkey in subkeys:
                                if subkey == vars_maquina[0].strip():
                                    tipo_dado = vars_maquina[1].strip()
                                    valor = vars_maquina[2]

                                    if tipo_dado == 'float':
                                        valor = float(valor)
                                    elif tipo_dado == 'str':
                                        valor = str(valor)
                                    elif tipo_dado == 'bool':
                                        valor = bool(valor)
                                    elif tipo_dado == 'int':
                                        valor = int(valor)
                                    else:
                                        valor = str(valor)
                                    json_arq[chave][subkey] = valor

                                    break
                        except:
                            pass

            # Transformaos a saida em string
            conteudo_saida = json.dumps(json_arq)
            comando = "sudo echo '"+conteudo_saida+"' | sudo tee "+path_json_saida_validador

            if emite_saida:
                saida_txt = saida_txt + comando + "\n\n"
            else:
                stdin, stdout, stderr = cliente.exec_command(comando)
                saida = stdout.read().decode("utf-8")
                erro = stdout.channel.recv_exit_status()
                stdin.flush()
                stdin.close()

                if reboot:
                    comando = "sudo pkill -9 -f python3 && sudo pkill -9 -f pyconcrete"
                    stdin, stdout, stderr = cliente.exec_command(comando)
                    saida = stdout.read().decode("utf-8")
                    erro = stdout.channel.recv_exit_status()
                    stdin.flush()
                    stdin.close()

        if saida_txt != '':
            return saida_txt
    except Exception as e:
        print(str(e))
        return ''

#print(troca_vars_cliente('cc-82-7f-31-82-85', '240507173025', 'param_elastic.json', False, True))
#print(troca_vars_cliente('cc-82-7f-31-82-85', '', 'param_elastic.json', False, True))

#print(troca_vars_arquivos('cc-82-7f-31-82-85', '240507173025', True))
#print(troca_vars_arquivos('cc-82-7f-31-82-85', '', True))

#print(gera_arq_troca_vars('cc-82-7f-31-82-85', '240507173025'))

#print(gera_arq_troca_vars('cc-82-7f-31-82-17'))

#os.system("clear")
#for maquina in maquinas_atualizar:
#    try:
#        print("Atualizando variaveis maquina "+maquina+"...")
#        #troca_vars_cliente('cc-82-7f-31-82-17', 'config.json')
#        troca_vars_arquivos(maquina)
#        print("Atualizadas variáveis maquina "+maquina)
#    except Exception as e:
#        print(str(e))


