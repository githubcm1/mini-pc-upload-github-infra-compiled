import os
import sys
from datetime import datetime
from time import sleep
import json
import funcoes
import subprocess

path = "/home/pi/mini-pc-upload-github-infra-compiled/"
path_releases_git = '/home/pi/cm_releases_git/'
path_aux_versao = path + "aux/"
path_releases_git_vars = '/home/pi/cm_releases_vars_git/'

header = "\033[33m############################################ GERANDO RELEASE ########################################\033[97m\n\n"

os.system("clear")
print(header)


print("Limpando releases anteriores")
os.system("sudo python3 "+path+"/limpa_releases_antigos.py")

os.system("sudo mkdir -p " + path_releases_git)

achou_ambiente = False
achou_file_maquinas = False
ambiente=""
file_maquinas = ""

gera_release = False

path_token = path + '/obtem_token.py'
output = subprocess.getoutput("sudo python3 "+path_token)
token = output.strip()


VALOR_VAR_PYCONCRETE="27cF#8yb2w3"

gera_versao_pyconcrete = False
atualiza_vars=False

for row in sys.argv:
    if row == "ambiente=dev" or row == "ambiente=hom" or row == "ambiente=prod" or row == 'ambiente=sandbox':
        achou_ambiente=True
        ambiente = row[9:30]
    
    if row == 'pyconcrete=yes':
        gera_versao_pyconcrete = True

    if row == "atualiza_vars=yes":
        atualiza_vars=True

if not achou_ambiente:
    print("Ambiente deve ser informado")
    quit()


try:
    comando = "sudo rm -rf "+path_aux_versao
    os.system(comando)
except Exception as e:
    pass

os.system("sudo mkdir -p "+path_aux_versao)

# Baixamos o conteudo do GIT
comando ="sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-" + ambiente + ".git " + path_aux_versao + "mini-pc-deploy-caixa-magica/"
os.system(comando)

# Pegamos a versao do fonte do GIT
with open(path_aux_versao+"mini-pc-deploy-caixa-magica/version.txt") as f:
    versao_git = f.read().strip()
f.close()


file_maquinas = path + "lista_maquinas/maquinas_" + ambiente + ".txt"

# Checa se o arquivo existe
if not os.path.exists(file_maquinas):
    print("Arquivo informado nao existe: " + str(file_maquinas))
    quit()
else:
    gera_release = True

if gera_release:
    sleep(1)

    try:
        with open(path + "/config/parametros.json") as json_data:
            aux = json.load(json_data)

            instala_apenas_dependencias = aux['instala_apenas_dependencias']
            instala_dependencias = aux['instala_dependencias']
            instala_pyconcrete = aux['instala_pyconcrete']
            atualiza_rec_facial = aux['atualiza_rec_facial']
            refaz_database = aux['refaz_database']
            obtem_linhas = aux['obtem_linhas']
            recarrega_contas = aux['recarrega_contas']
            faz_reboot = aux['faz_reboot']
            mantem_tabelas_contas = aux['mantem_tabelas_contas']
    except Exception as e:
        instala_apenas_dependencias = False
        instala_dependencias = True
        instala_pyconcrete = True
        atualiza_rec_facial = True
        refaz_database = True
        obtem_linhas = True
        recarrega_contas = True
        faz_reboot = True
        mantem_tabelas_contas = False

    # Gera o release pelo timestamp atual
    release = datetime.utcnow().strftime("%y%m%d%H%M%S")
    path_release = path + "/releases/" + release + "/"
    path_maquinas = path_release + "/lista_maquinas/"
    path_comandos = path_release + "/lista_comandos/"
    file_comandos = path_comandos + "/comandos.txt"

    # Baixamos o conteudo do GIT
    path_releases_git_vars = path_releases_git_vars + release
    os.system('sudo mkdir -p '+path_releases_git_vars)
    comando ="sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-vars-" + ambiente + ".git " + path_releases_git_vars
    os.system(comando)

    # Cria dir do release
    os.system("sudo mkdir -p " + path_release)

    # Cria dir com lista de maquinas para este release
    os.system("sudo mkdir -p " + path_maquinas)
    os.system("sudo cp " + file_maquinas + " " + path_maquinas + "/maquinas.txt")

    # Checamos aqui se o numero de maquinas ultrapassa o limite permitido da release
    atingiu_limite_maquinas = funcoes.check_excesso_maquinas_release(release)

    if atingiu_limite_maquinas:
        print("Release " + str(release) + " esta com um numero de maquinas maior do que o permitido. Revise lista de maquinas e tente novamente.")
        quit()

    # Cria dir com os comandos necessarios
    os.system("sudo mkdir -p " + path_comandos)
    os.system("sudo touch " + file_comandos)

    comandos = ['sudo pkill -9 -f python3',
                'sudo pkill -9 -f start_monitor',
                'sudo pkill -9 -f pyconcrete',
                'sleep 0.5',
                'echo "Instalando PyConcrete"',
                'sudo rm -rf /home/pi/pyconcrete/',
                'sudo mkdir -p /home/pi/pyconcrete/',
                'cd /home/pi/pyconcrete/',
                'sudo git clone https://github.com/Falldog/pyconcrete.git /home/pi/pyconcrete/',
                'echo "Pyconcrete instalado!"',
                'echo "Iniciando setup de chave criptografica PyConcrete"',
                'cd /home/pi/pyconcrete/',
                'sudo printf \"' +VALOR_VAR_PYCONCRETE + '\\n' + VALOR_VAR_PYCONCRETE +'" | sudo python3 setup.py install',
                'echo "Setup Pyconcrete finalizado"'
                ]

    if atualiza_vars:
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica-vars/")
    comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/")
    comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica-share/")
    comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica-rec-facial/")

    folder = '/home/pi/'

    if atualiza_vars:
        comandos.append("sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-vars-" + ambiente + ".git " + folder + "mini-pc-deploy-caixa-magica-vars/")
        sleep(5)
    comandos.append("sudo git clone https://" + token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-" + ambiente + ".git " + folder + "mini-pc-deploy-caixa-magica/")

    if gera_versao_pyconcrete:
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/*.pye")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/sincronismo/*.pye")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/tela/*.pye")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/core/*.pye")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/scripts_bd/*.pye")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/teste_hw/*.pye")

        comandos.append("cd /home/pi/mini-pc-deploy-caixa-magica/")
        comandos.append("sudo grep -rli 'python3' * | xargs -i@ sudo sed -i 's/python3/pyconcrete/g' @")
        comandos.append("sudo grep -rli '\.py' * | xargs -i@ sudo sed -i 's/\.py/\.pye/g' @")
        comandos.append("sudo grep -rli '\pyeplot' * | xargs -i@ sudo sed -i 's/\pyeplot/\pyplot/g' @")

        comandos.append('sudo python3 /home/pi/pyconcrete/pyconcrete-admin.py compile --source="/home/pi/mini-pc-deploy-caixa-magica/" --pye')
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/*.py")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/sincronismo/*.py")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/tela/*.py")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/core/*.py")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/scripts_bd/*.py")
        comandos.append("sudo rm -rf /home/pi/mini-pc-deploy-caixa-magia/teste_hw/*.py")


    if instala_apenas_dependencias:
        instala_dependencias = True

    if instala_dependencias:
        comandos.append("sudo sh /home/pi/mini-pc-deploy-caixa-magica/dependencias_so/instala_dependencias.sh")

    if instala_apenas_dependencias:
        comandos.append("sudo reboot -f")


    # Copiando script de instalacao atual
    comandos.append("sudo mkdir -p /home/pi/instalacao_bkp/")
    comandos.append("sudo cp /home/pi/caixa-magica-operacao/instalacao.json /home/pi/instalacao_bkp/")
    comandos.append("sudo cp /home/pi/caixa-magica-operacao/sincronismo.json /home/pi/instalacao_bkp/")
    comandos.append("sudo rm -rf /home/pi/caixa-magica-operacao/")

    if atualiza_vars:
        comandos.append("sudo rm -rf /home/pi/caixa-magica-vars/")
    comandos.append("sudo rm -rf /home/pi/caixa-magica/")

    if atualiza_rec_facial:
        comandos.append("sudo rm -rf /home/pi/caixa-magica-rec-facial/")
        comandos.append("sudo rm -rf /home/pi/caixa-magica-share/")

    comandos.append("sudo rm -rf /home/pi/caixa-magica-logs/")
    comandos.append("sudo rm -rf /home/pi/caixa-magica-img/")

    comandos.append("sudo mkdir -p /home/pi/caixa-magica-img/")
    comandos.append("sudo mkdir -p /home/pi/caixa-magica-logs/")
    comandos.append("sudo mkdir -p /home/pi/caixa-magica-operacao/")

    comandos.append("sudo cp /home/pi/instalacao_bkp/instalacao.json /home/pi/caixa-magica-operacao/")
    comandos.append("sudo cp /home/pi/instalacao_bkp/sincronismo.json /home/pi/caixa-magica-operacao/")

    if atualiza_rec_facial:
        comandos.append("sudo git clone https://"+ token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-rec-facial-"+ambiente+".git " + folder + "mini-pc-deploy-caixa-magica-rec-facial/")
        comandos.append("sudo git clone https://"+ token + "@github.com/githubcm1/mini-pc-deploy-caixa-magica-share-"+ambiente+".git " + folder + "mini-pc-deploy-caixa-magica-share/")

    if atualiza_vars:
        comandos.append("sudo mv /home/pi/mini-pc-deploy-caixa-magica-vars/ /home/pi/caixa-magica-vars/")
    comandos.append("sudo mv /home/pi/mini-pc-deploy-caixa-magica/ /home/pi/caixa-magica/")

    if atualiza_rec_facial:
        comandos.append("sudo mv /home/pi/mini-pc-deploy-caixa-magica-rec-facial/ /home/pi/caixa-magica-rec-facial/")
        comandos.append("sudo mv /home/pi/mini-pc-deploy-caixa-magica-share/ /home/pi/caixa-magica-share/")

    comandos.append("sudo sh /home/pi/caixa-magica/tela_instalacao.sh &")
    
    if gera_versao_pyconcrete:
        comandos.append("sudo pyconcrete /home/pi/caixa-magica/start_conf_db.pye")
    else:
        comandos.append("sudo python3 /home/pi/caixa-magica/start_conf_db.py")

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

    # Coloca, dentro da pasta de caixa magica, o release efetuado
    comandos.append("sudo rm -rf /home/pi/caixa-magica/releases/")
    comandos.append("sudo mkdir -p /home/pi/caixa-magica/releases/")
    comandos.append("sudo touch /home/pi/caixa-magica/releases/" + release + ".txt")
    comandos.append("sudo mkdir -p /home/pi/caixa-magica-vars/")

    path_release_destino = "/home/pi/releases_cm/" + release + "/"
    comandos.append('cd '+path_release_destino)

    # Aloca aqui um conteudo, que devera ser substituido pelo script de variaveis
    comandos.append("SCRIPT_VARS")

    comandos.append("echo \"Script atualizacao executado\"")

    # registra, na maquina destino, a execucao da atualizacao
    comandos.append("sudo mkdir -p " + path_release_destino)
    comandos.append("sudo touch " + path_release_destino + "/executado.txt")

    # Remove da cron
    comandos.append('( crontab -l | grep -v -F "logs_executa.txt" ) | crontab -')
    comandos.append('sudo rm -f /home/pi/releases_cm/' + release +'/executa.sh')

    if faz_reboot:
        comandos.append("sudo reboot -f")


    # Grava cada linha no arquivo de comandos da release
    with open(file_comandos, 'a') as fil:
        for linha in comandos:
            fil.write(linha + "\n")
    fil.close()

    file_comandos_releases_git = path_releases_git + "/" + release + "_comandos.txt"
    os.system("sudo cp " + file_comandos + " " + file_comandos_releases_git)

    # agenda cron no lado do cliente
    file_agenda = path_releases_git + "/" + release + "_agenda_cron.sh"
    os.system("sudo rm -f " + file_agenda)
    os.system("sudo touch " + file_agenda)
    comandos_cron = []

    file_versao = path_releases_git + "/" + release + "_version.txt"
    with open(file_versao, "w") as f:
        f.write(versao_git)
    f.close()

    comandos_cron.append("sudo mkdir -p /home/pi/.config/autostart/")
    ##comandos_cron.append("sudo cp -f /home/pi/caixa-magica/templates/autostart/auto.desktop.instala /home/pi/.config/autostart")

    comandos_cron.append('croncmd="sudo sh ' + path_release_destino + '/executa.sh > ' + path_release_destino + '/logs_executa.txt 2>&1"')
    comandos_cron.append('cronjob="MIN HORA DIA MES * $croncmd"')
    comandos_cron.append('( crontab -l | grep -v -F "logs_executa.txt" ) | crontab -')
    comandos_cron.append('( crontab -l | grep -v -F "$croncmd" ; echo "$cronjob" ) | crontab -')

    with open(file_agenda, 'a') as fil:
        for com_exec in comandos_cron:
            fil.write(com_exec + "\n")
    fil.close()

    # Sobe no GIT
    os.system("cd " + path_releases_git + " ; sudo git init ; sudo git add . ; sudo git commit -m \"Commit CM\" ; sudo git branch -M main ; sudo git remote remove origin_cm_releases_git ; sudo git remote add origin_cm_releases_git git@github.com:githubcm1/mini-pc-releases-comandos.git ; sudo git push origin_cm_releases_git main --force")

    os.system("clear")
    print(header)
    print("Release: " + release + " (ambiente: " + ambiente + ")\n\n")
