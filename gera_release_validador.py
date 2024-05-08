import os
import sys
from datetime import datetime
from time import sleep
import json
import funcoes
import subprocess

path = "/home/pi/mini-pc-upload-github-infra-compiled/"
path_releases_git = '/home/pi/cm_releases_validador_git/'

os.system("clear")

os.system("sudo mkdir -p " + path_releases_git)

achou_ambiente = False
achou_file_maquinas = False
ambiente=""
file_maquinas = ""
folder = '/home/pi/'
folder_deploy = '/home/pi/deploy-caixa-magica/'
operadoraid = ""

gera_release = False

# ESTE TOKEN EH O DA CONTA githubcm1
path_token = path + '/obtem_token.py'
output = subprocess.getoutput("sudo python3 "+path_token)
token = output.strip()

VALOR_VAR_PYCONCRETE="27cF#8yb2w3"

gera_versao_pyconcrete = False

for row in sys.argv:
    if row == "ambiente=dev" or row == "ambiente=hom" or row == "ambiente=prod":
        achou_ambiente=True
        ambiente = row[9:30]
    
    if row == 'pyconcrete=yes':
        gera_versao_pyconcrete = True

    if 'operadora=' in row:
        operadoraid = row[10:40]

if not achou_ambiente:
    print("Ambiente deve ser informado")
    quit()

if operadoraid == "":
    print("Operadora deve ser informada")
    quit()

# Define o usuario github de acesso
git_account = 'githubcm1'

path_releases_git = path_releases_git + ambiente + "/" + str(operadoraid) + "/"
os.system("sudo mkdir -p " + path_releases_git)

# Limpa o diretorio, para garantir que fique apenas o ultimo release
os.system("sudo rm -rf " + path_releases_git + "/*")

# Recria o diretorio
comando = 'sudo rm -rf ' + folder_deploy
os.system(comando)
comando ='sudo mkdir -p ' + folder_deploy
os.system(comando)

# Atraves do ambiente informado, pegamos a versao da aplicacao
comando = "sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-" + ambiente + ".git " + folder_deploy
os.system(comando)

# Pela versao obtida, colocamos o nome do release
with open(folder_deploy + "/version.txt") as fil:
    conteudo = fil.readlines()
    prefixo_release =path_releases_git + "/" + str(conteudo[0])

INTERACAO = 1

while INTERACAO <= 2:
   
    # Se for a primeira interacao, colocamos o nome do release com as dependencias
    if INTERACAO == 1:
        file_release = prefixo_release + "_FULL.sh"
    else:
        file_release = prefixo_release + "_VERSAO.sh"

    file_release_binary = file_release[0:len(file_release)-3]
    os.system("sudo rm -f " + file_release)
    os.system("sudo rm -f " + file_release_binary)

    # Se for a primeira interacao, entendemos que trata-se do script  
    if INTERACAO == 1:
        instala_apenas_dependencias = False
        instala_dependencias = True
        instala_pyconcrete = True
        refaz_database = False
        obtem_linhas = True
        recarrega_contas = False
        faz_reboot = True
        mantem_tabelas_contas = True
    else:
        instala_apenas_dependencias = False
        instala_dependencias = False
        instala_pyconcrete = True
        refaz_database = False
        obtem_linhas = True
        recarrega_contas = False
        faz_reboot = True
        mantem_tabelas_contas = True
                
    comandos =  ['#!/bin/bash',
                'sudo pkill -9 -f start_monitor',
                'sleep 0.5',
                'echo "Instalando PyConcrete"',
                'sudo rm -rf /home/pi/pyconcrete/',
                'sudo mkdir -p /home/pi/pyconcrete/',
                'cd /home/pi/pyconcrete/',
                'sudo git clone https://github.com/Falldog/pyconcrete.git /home/pi/pyconcrete/ > /dev/null 2>&1',
                'echo "Pyconcrete instalado!"',
                'echo "Iniciando setup de chave criptografica PyConcrete"',
                'cd /home/pi/pyconcrete/',
                'sudo printf \"' +VALOR_VAR_PYCONCRETE + '\\n' + VALOR_VAR_PYCONCRETE +'" | sudo python3 /home/pi/pyconcrete/setup.py install',
                'echo "Setup Pyconcrete finalizado"'
                ]

    comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica-vars/")
    comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/")
    comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica-share/")
    comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica-rec-facial/")

    folder = '/home/pi/'
    comandos.append('echo "Baixando VARS"')
    comandos.append("sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-vars-" + ambiente + ".git " + folder + "deploy-caixa-magica-vars/ > /dev/null 2>&1")
    comandos.append('echo "Baixando Codigo Sistema"')
    comandos.append("sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-" + ambiente + ".git " + folder + "deploy-caixa-magica/ > /dev/null 2>&1")

    if gera_versao_pyconcrete:
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/*.pye")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/sincronismo/*.pye")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/tela/*.pye")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/core/*.pye")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/scripts_bd/*.pye")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/teste_hw/*.pye")

        comandos.append("cd /home/pi/deploy-caixa-magica/")
        comandos.append("sudo grep -rli 'python3' * | xargs -i@ sudo sed -i 's/python3/pyconcrete/g' @")
        comandos.append("sudo grep -rli '\.py' * | xargs -i@ sudo sed -i 's/\.py/\.pye/g' @")
        comandos.append("sudo grep -rli '\pyeplot' * | xargs -i@ sudo sed -i 's/\pyeplot/\pyplot/g' @")

        comandos.append('sudo python3 /home/pi/pyconcrete/pyconcrete-admin.py compile --source="/home/pi/deploy-caixa-magica/" --pye')
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/*.py")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/sincronismo/*.py")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/tela/*.py")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/core/*.py")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magica/scripts_bd/*.py")
        comandos.append("sudo rm -rf /home/pi/deploy-caixa-magia/teste_hw/*.py")

    if instala_dependencias:
        comandos.append("sudo sh /home/pi/deploy-caixa-magica/dependencias_so/instala_dependencias.sh")

    # Copiando script de instalacao atual
    comandos.append("sudo mkdir -p /home/pi/instalacao_bkp/")
    comandos.append("sudo cp /home/pi/caixa-magica-operacao/instalacao.json /home/pi/instalacao_bkp/")
    comandos.append("sudo cp /home/pi/caixa-magica-operacao/sincronismo.json /home/pi/instalacao_bkp/")
    comandos.append("sudo rm -rf /home/pi/caixa-magica-operacao/")

    comandos.append("sudo rm -rf /home/pi/caixa-magica-vars/")
    comandos.append("sudo rm -rf /home/pi/caixa-magica/")

    comandos.append("sudo rm -rf /home/pi/caixa-magica-rec-facial/")
    comandos.append("sudo rm -rf /home/pi/caixa-magica-share/")

    comandos.append("sudo rm -rf /home/pi/caixa-magica-logs/")
    comandos.append("sudo rm -rf /home/pi/caixa-magica-img/")

    comandos.append("sudo mkdir -p /home/pi/caixa-magica-img/")
    comandos.append("sudo mkdir -p /home/pi/caixa-magica-logs/")
    comandos.append("sudo mkdir -p /home/pi/caixa-magica-operacao/")

    comandos.append("sudo cp /home/pi/instalacao_bkp/instalacao.json /home/pi/caixa-magica-operacao/")
    comandos.append("sudo cp /home/pi/instalacao_bkp/sincronismo.json /home/pi/caixa-magica-operacao/")

    comandos.append('echo "Baixando bibliotecas Rec Facial"')
    comandos.append("sudo git clone https://"+ token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-rec-facial-"+ambiente+".git " + folder + "deploy-caixa-magica-rec-facial/ > /dev/null 2>&1")
    comandos.append("sudo git clone https://"+ token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-share-"+ambiente+".git " + folder + "deploy-caixa-magica-share/ > /dev/null 2>&1")

    comandos.append("sudo mv /home/pi/deploy-caixa-magica-vars/ /home/pi/caixa-magica-vars/")
    comandos.append("sudo mv /home/pi/deploy-caixa-magica/ /home/pi/caixa-magica/")

    comandos.append("sudo mv /home/pi/deploy-caixa-magica-rec-facial/ /home/pi/caixa-magica-rec-facial/")
    comandos.append("sudo mv /home/pi/deploy-caixa-magica-share/ /home/pi/caixa-magica-share/")

    comandos.append("sudo sh /home/pi/caixa-magica/tela_instalacao.sh &")
    
    if gera_versao_pyconcrete:
        comandos.append("sudo pyconcrete /home/pi/caixa-magica/start_conf_db.pye > /dev/null 2>&1")
    else:
        comandos.append("sudo python3 /home/pi/caixa-magica/start_conf_db.py > /dev/null 2>&1")

    if refaz_database:
        params = ""
        if mantem_tabelas_contas:
            params= params + " --mantem_contas=S "

        if gera_versao_pyconcrete:
            comandos.append("sudo pyconcrete /home/pi/caixa-magica/scripts_bd/script_bd_drop.pye " + params)
            comandos.append("sudo pyconcrete /home/pi/caixa-magica/scripts_bd/script_bd.pye")
        else:
            comandos.append("sudo python3 /home/pi/caixa-magica/scripts_bd/script_bd_drop.py " + params)
            comandos.append("sudo python3 /home/pi/caixa-magica/scripts_bd/script_bd.py")

    if obtem_linhas:
        if gera_versao_pyconcrete:
            comandos.append("sudo pyconcrete /home/pi/caixa-magica/sincronismo/sincronismo_obtem_linhas.pye force")
        else:
            comandos.append("sudo python3 /home/pi/caixa-magica/sincronismo/sincronismo_obtem_linhas.py force")

    if recarrega_contas:
        #comandos.append("sudo python3 /home/pi/caixa-magica/sincronismo/sincronismo_contingencia_contas.py")
        comandos.append("sudo rm -rf /home/pi/caixa-magica-operacao/sincronismo.json")

        # reseta as tabelas de contas caso a atualizacao tenha sido parametrizada assim
        if not mantem_tabelas_contas:
            if gera_versao_pyconcrete:
                comandos.append("sudo pyconcrete /home/pi/caixa-magica/reset_contas.pye")
            else:
                comandos.append("sudo python3 /home/pi/caixa-magica/reset_contas.py")

    # Mantem a viagem aberta, caso ainda haja alguma no banco de dados
    if gera_versao_pyconcrete:
        comandos.append("sudo pyconcrete /home/pi/caixa-magica/mantem_viagem_aberta.pye")
    else:
        comandos.append("sudo python3 /home/pi/caixa-magica/mantem_viagem_aberta.py")

    if faz_reboot:
        comandos.append("sudo reboot -f")

    with open(file_release, 'a') as fil:
        for com_exec in comandos:
            fil.write(com_exec + "\n")
    fil.close()

    # geramos o binario do script SH
    os.system("sudo shc -f " + file_release + " -o " + file_release_binary)

    # Eliminamos os eventuais arquivos .SH que ficaram
    os.system("sudo rm -rf " + file_release + "*")

    INTERACAO = INTERACAO +1 
    
# Sobe no GIT
comando =("cd " + path_releases_git + " ; sudo git init ; sudo git add . ; sudo git commit -m \"Commit CM\" ; sudo git branch -M main ; sudo git remote remove origin_cm_releases_git ; sudo git remote add origin_cm_releases_git git@github.com:" + git_account + "/release_validador_" + ambiente + "_" + str(operadoraid)+ ".git ; sudo git push origin_cm_releases_git main --force")
os.system(comando)

os.system("clear")
print("Release gerado. Checar em sua conta github '" + git_account + "'")
