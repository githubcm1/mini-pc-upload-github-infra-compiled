clear
var_ambiente=""
var_username_git="githubcm1"
var_email_git="githubcm1@gmail.com"

aux=`sudo python3 /home/pi/mini-pc-upload-github-infra-compiled/obtem_token.py`
token="$aux"

if [ -z "$1" ]; then
  echo "Parametro ambiente nao informado"
  exit
fi

if [ "$1" = "ambiente=dev" ]; then
  var_ambiente="DEV"
  sufixo_api="dev.buspay.com.br"
  sufixo_git="dev"
fi
if [ "$1" = "ambiente=hom" ]; then
  var_ambiente="HOM"
  sufixo_api="homolog.buspay.com.br"
  sufixo_git="hom"

fi
if [ "$1" = "ambiente=prod" ]; then
  var_ambiente="PROD"
  sufixo_api="buspay.com.br"
  sufixo_git="prod"
fi
if [ "$1" = "ambiente=sandbox" ]; then
  var_ambiente="SANDBOX"
  sufixo_api="dev.buspay.com.br"
  sufixo_git="sandbox"
fi

if [ -z "$var_ambiente" ]; then
   echo "Ambiente especificado nao informado (use 'dev', 'hom' ou 'prod')"
   exit
fi

echo "Recriando diretorios de deploy"
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/
sudo mkdir -p /home/pi/mini-pc-deploy-caixa-magica/

sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica-vars/
sudo mkdir -p /home/pi/mini-pc-deploy-caixa-magica-vars/

sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica-rec-facial/
sudo mkdir -p /home/pi/mini-pc-deploy-caixa-magica-rec-facial/

echo "Recriando diretorios de fontes"
sudo rm -rf /home/pi/mini-pc-src-caixa-magica/
sudo mkdir -p /home/pi/mini-pc-src-caixa-magica/

sudo rm -rf /home/pi/mini-pc-src-caixa-magica-vars/
sudo mkdir -p /home/pi/mini-pc-src-caixa-magica-vars/

sudo rm -rf /home/pi/mini-pc-src-caixa-magica-rec-facial/
sudo mkdir -p /home/pi/mini-pc-src-caixa-magica-rec-facial/

# Se a acao informada for de um ambiente "DEV", devemos considerar que o deploy sera feito a partir do mesmo fonte carregado pelo desenvolvedor
# Se a acao informada for de um ambiente "HOM", entao devemos primeiro pegar o ocnteudo do fonte de dev e atualizar o de homolog
# Se a acao informada for de um ambiente "PROD", entao devemos primeiro pegar o ocnteudo do fonte de hom e atualizar o de prod
echo "Baixando conteudo dos fontes da origem"

# Se for ambiente SANDBOX, baixamos o conteudo de SANDBOX
if [ "$var_ambiente" = "SANDBOX" ] || [ "$var_ambiente" = "DEV" ]; then
   cd /home/pi/mini-pc-src-caixa-magica/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-sandbox.git
   sudo mv mini-pc-src-caixa-magica-sandbox/* .
   sudo rm -rf mini-pc-src-caixa-magica-sandbox/

   cd /home/pi/mini-pc-src-caixa-magica-vars/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-vars-sandbox.git
   sudo mv mini-pc-src-caixa-magica-vars-sandbox/* .
   sudo rm -rf mini-pc-src-caixa-magica-vars-sandbox/

   cd /home/pi/mini-pc-src-caixa-magica-rec-facial/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-rec-facial-sandbox.git
   sudo mv mini-pc-src-caixa-magica-rec-facial-sandbox/* .
   sudo rm -rf mini-pc-src-caixa-magica-rec-facial-sandbox/
fi

#exit

if [ "$var_ambiente" = "HOM" ]; then
   # Baixa o conteudo do fonte de dev
   cd /home/pi/mini-pc-src-caixa-magica/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-dev.git
   sudo mv mini-pc-src-caixa-magica-dev/* .
   sudo rm -rf mini-pc-src-caixa-magica-dev/

   cd /home/pi/mini-pc-src-caixa-magica-vars/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-vars-dev.git
   sudo mv mini-pc-src-caixa-magica-vars-dev/* .
   sudo rm -rf mini-pc-src-caixa-magica-vars-dev/

   cd /home/pi/mini-pc-src-caixa-magica-rec-facial/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-rec-facial-dev.git
   sudo mv mini-pc-src-caixa-magica-rec-facial-dev/* .
   sudo rm -rf mini-pc-src-caixa-magica-rec-facial-dev/
fi

if [ "$var_ambiente" = "PROD" ]; then
   # Baixa o conteudo do fonte de dev
   cd /home/pi/mini-pc-src-caixa-magica/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-hom.git
   sudo mv mini-pc-src-caixa-magica-hom/* .
   sudo rm -rf mini-pc-src-caixa-magica-hom/

   cd /home/pi/mini-pc-src-caixa-magica-vars/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-vars-hom.git
   sudo mv mini-pc-src-caixa-magica-vars-hom/* .
   sudo rm -rf mini-pc-src-caixa-magica-vars-hom/

   cd /home/pi/mini-pc-src-caixa-magica-rec-facial/
   sudo git clone https://$token@github.com/githubcm1/mini-pc-src-caixa-magica-rec-facial-hom.git
   sudo mv mini-pc-src-caixa-magica-rec-facial-hom/* .
   sudo rm -rf mini-pc-src-caixa-magica-rec-facial-hom/
fi

# Aplicamos aqui a configuracao de ambiente forcadamente
sudo sed -i '/urlbase=/d' /home/pi/mini-pc-src-caixa-magica/core/endpoints.py
sudo sed -i '/urladm=/d' /home/pi/mini-pc-src-caixa-magica/core/endpoints.py

sudo echo 'urlbase="https://api-operacao.'$sufixo_api'/"' | sudo tee -a /home/pi/mini-pc-src-caixa-magica/core/endpoints.py
sudo echo 'urladm="https://api-administracao.'$sufixo_api'/"' | sudo tee -a /home/pi/mini-pc-src-caixa-magica/core/endpoints.py

sudo python3 /home/pi/mini-pc-upload-github-infra-compiled/determina_versao_env.py

################# CARGA DOS FONTES
# subimos o codigo no ambiente de fonte homolog
cd /home/pi/mini-pc-src-caixa-magica/
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_caixa-magica
sudo git remote add origin_caixa-magica git@github.com:$var_username_git/mini-pc-src-caixa-magica-$sufixo_git.git
sudo git push origin_caixa-magica main --force  	

cd /home/pi/mini-pc-src-caixa-magica-vars/
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_caixa-magica-vars
sudo git remote add origin_caixa-magica-vars git@github.com:$var_username_git/mini-pc-src-caixa-magica-vars-$sufixo_git.git
sudo git push origin_caixa-magica-vars main --force

cd /home/pi/mini-pc-src-caixa-magica-rec-facial/
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_caixa-magica-rec-facial
sudo git remote add origin_caixa-magica-rec-facial git@github.com:$var_username_git/mini-pc-src-caixa-magica-rec-facial-$sufixo_git.git
sudo git push origin_caixa-magica-rec-facial main --force

######################## CARGA DO DEPLOY 

echo "TRECHO DEPLOY"

# Copia o fonte pra pasta de deploy (mexer depois, porque aqui devera entrar a parte do pyconcrete
sudo cp -rf /home/pi/mini-pc-src-caixa-magica/* /home/pi/mini-pc-deploy-caixa-magica/
sudo cp -rf /home/pi/mini-pc-src-caixa-magica-vars/* /home/pi/mini-pc-deploy-caixa-magica-vars/
sudo cp -rf /home/pi/mini-pc-src-caixa-magica-rec-facial/* /home/pi/mini-pc-deploy-caixa-magica-rec-facial/

# Removendo PYE do diretorio de caixa magica
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/*.pye
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/sincronismo/*.pye
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/tela/*.pye
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/core/*.pye
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/scripts_bd/*.pye
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/teste_hw/*.pye

cd /home/pi/mini-pc-deploy-caixa-magica
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_caixa-magica
sudo git remote add origin_caixa-magica git@github.com:$var_username_git/mini-pc-deploy-caixa-magica-$sufixo_git.git
sudo git push origin_caixa-magica main --force

cd /home/pi/mini-pc-deploy-caixa-magica-vars/
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_caixa-magica-vars
sudo git remote add origin_caixa-magica-vars git@github.com:$var_username_git/mini-pc-deploy-caixa-magica-vars-$sufixo_git.git
sudo git push origin_caixa-magica-vars main --force

cd /home/pi/mini-pc-deploy-caixa-magica-rec-facial/
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_caixa-magica-rec-facial
sudo git remote add origin_caixa-magica-rec-facial git@github.com:$var_username_git/mini-pc-deploy-caixa-magica-rec-facial-$sufixo_git.git
sudo git push origin_caixa-magica-rec-facial main --force

sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica/
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica-vars/
sudo rm -rf /home/pi/mini-pc-deploy-caixa-magica-rec-facial/
sudo rm -rf /home/pi/mini-pc-src-caixa-magica/
sudo rm -rf /home/pi/mini-pc-src-caixa-magica-vars/
sudo rm -rf /home/pi/mini-pc-src-caixa-magica-rec-facial/

echo "Finalizado"

