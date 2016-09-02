#!/usr/bin/python

# importo rutinas para trabajar con el sistema operativo
import os
from os import listdir
from os.path import isfile, join

# importo rutinas de expresiones regulares
import re

# genero los paths para los directorios base
script_dir = os.path.dirname(__file__)
data_path  = "data"
abs_file_path = os.path.join(script_dir, data_path)

# declaro los paths para los dos archivos
rcv_path = os.path.join(abs_file_path, 'last-image-rcv')
prs_path = os.path.join(abs_file_path, 'last-image-prs')

# abro los dos archivos para trabajar con ellos
# el primero es de solo lectura, y el segundo es de lectura escritura
ultima_recibida  = open(rcv_path, 'r')
ultima_procesada = open(prs_path, 'r+')

# para cada linea del archivo, la imprimo
for line in ultima_recibida:
  print line

# para cada linea del archivo, la imprimo
for line in ultima_procesada:
  print line

# 2016.09.245.163507
# 2016.09.244.163507

pattern = re.compile(".*prs.*")

# listo solo los archivos del path elegido y que cumplen la expresion regular
files_in_dir = [f for f in listdir(abs_file_path)
                if isfile(join(abs_file_path, f)) and
                pattern.match(f)
               ]

print files_in_dir
