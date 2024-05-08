#!/bin/bash
clear
var_username_git="githubcm1"

aux=`sudo cat /home/pi/mini-pc-upload-github-infra-compiled/token_push.txt`
token="$aux"

clear

sudo rm -rf /home/pi/mini-pc-upload-github-infra-compiled/token_push.txt
sudo touch /home/pi/mini-pc-upload-github-infra-compiled/token_push.txt
sudo rm -rf /home/pi/mini-pc-upload-github-infra-compiled/releases/*
cd /home/pi/mini-pc-upload-github-infra-compiled/
sudo rm -rf .git
sleep 1
sudo git init
sudo git add .
sudo git commit -m "Commit CM"
sudo git branch -M main
sudo git remote remove origin_upload-github
sudo git remote add origin_upload-github git@github.com:$var_username_git/mini-pc-upload-github-infra-compiled.git
sudo git push origin_upload-github main --force

sleep 1
sudo echo $token | sudo tee /home/pi/mini-pc-upload-github-infra-compiled/token_push.txt
clear
echo "Versionado. Conferir github.com:$var_username_git/mini-pc-upload-github-infra-compiled.git"
