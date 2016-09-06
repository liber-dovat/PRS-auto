#!/usr/bin/python

# importo el modulo funciones
import funciones
from datetime import date, timedelta, datetime

# importo rutinas para trabajar con el sistema operativo
import os
from   os      import listdir
from   os.path import isfile, join

# importo rutinas de expresiones regulares
import re

#########################################
#########################################
# Defino las rutas a los archivos para poder trabajar con ellos
#########################################

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

#########################################
#########################################
# Recorro las lineas de los documentos y las imprimo
#########################################

# para cada linea del archivo, la imprimo
for line in ultima_recibida:
  print line
  # tomo la linea y genero un arreglo con sus palabras
  rcv_split = line.split(".")
# for

# para cada linea del archivo, la imprimo
for line in ultima_procesada:
  print line
  # tomo la linea y genero un arreglo con sus palabras
  prs_split = line.split(".")
# for

# 2016.09.245.163507
# 2016.09.244.163507

#########################################
#########################################
# Realizo operaciones de impresion en pantalla para ver los parametros
#########################################

print rcv_split
print prs_split

rcv_year = int(rcv_split[0]) # la primer palabra del arreglo es el ano
prs_year = int(prs_split[0]) # la primer palabra del arreglo es el ano

rcv_doy = int(rcv_split[2]) # la tercera palabra del arreglo es el doy
prs_doy = int(prs_split[2]) # la tercera palabra del arreglo es el doy

#########################################
#########################################
# Genero los datatypes date para iterar entre ellos y leo las carpetas
#########################################

start_ymd     = funciones.ymd(prs_year,prs_doy)
starting_date = datetime(prs_year, start_ymd[1],start_ymd[2] + 1, 16, 35, 07)

ending_ymd  = funciones.ymd(rcv_year,rcv_doy)
ending_date = datetime(rcv_year, ending_ymd[1], ending_ymd[2], 18, 25, 05)

delta = timedelta(seconds=1)
rango_fechas = funciones.datespan(starting_date, ending_date, delta)

# for f in rango_fechas:
#   print f

for day in rango_fechas:

  # Path a los raw
  path_string = "/sat/raw-sat/" + str(day[0]) + "/" + str(day[1]).zfill(2) + "/"
  data_path   = os.path.abspath(path_string)

  # day[0] se corresponde con el ano, y day[2] corresponde al doy
  # el patron queda .*year\.doy.*\.nc
  string_patron = ".*" + str(day[0]) + "\." + str(day[2]).zfill(3) + ".*" + "\.nc$"
  pattern       = re.compile(string_patron)

  # listo solo los archivos del path elegido y que cumplen la expresion regular
  files_in_dir = [f for f in listdir(data_path)
                   if isfile(join(data_path, f)) and pattern.match(f)
                 ] # for f in

  for f in files_in_dir:
    print path_string + f
# for day in rango_fechas 
