#!/bin/bash
sudo pkill -9 -f dispara_release.py
sleep 1
sudo rm release_em_exec.txt
clear
cd /home/pi/mini-pc-upload-github-infra-compiled/
sudo python3 dispara_release.py $1
