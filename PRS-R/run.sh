#!/bin/bash

# Black        0;30     Dark Gray     1;30
# Red          0;31     Light Red     1;31
# Green        0;32     Light Green   1;32
# Brown/Orange 0;33     Yellow        1;33
# Blue         0;34     Light Blue    1;34
# Purple       0;35     Light Purple  1;35
# Cyan         0;36     Light Cyan    1;36
# Light Gray   0;37     White         1;37

RED='\033[0;31m'
NC='\033[0m' # No Color

export PROJ_LIB=/usr/local/share/proj
export PROJ_DEBUG=0

echo -e "Ejecutando: ${RED}time make clean && make && ./exec_auto.sh && ./plot/convertir_imgs.py${NC}"

# rm /home/ldovat/dev/PRS-sat/PRS-R/plot/png/B01-FR/2018/ART_2018302_180037.png
# time make clean && make && ./exec_auto.sh && ./plot/convertir_imgs.py
make clean && time make && time ./exec_auto.sh