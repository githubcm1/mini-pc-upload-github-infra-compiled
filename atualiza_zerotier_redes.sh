#!/bin/bash
clear
echo "Subindo configuracao de redes x empresas"
sleep 1
var_ambiente=""
var_username_git="githubcm1"
var_email_git="githubcm1@gmail.com"

aux=`sudo python3 /home/pi/mini-pc-upload-github-infra-compiled/obtem_token.py`
token="$aux"

################# CARGA DOS FONTES
# subimos o codigo no ambiente de fonte homolog
cd /home/pi/zerotier_redes/
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_zerotier_redes
sudo git remote add origin_zerotier_redes git@github.com:$var_username_git/zerotier_redes.git
sudo git push origin_zerotier_redes main --force  	

clear
echo "Finalizado"
