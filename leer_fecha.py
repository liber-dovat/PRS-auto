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
script_dir    = os.path.dirname(__file__)
data_path     = "data"
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

rcv_hms = rcv_split[3] # la cuarta palabra del arreglo es la hora-minuto-segundo
prs_hms = prs_split[3] # la cuarta palabra del arreglo es la hora-minuto-segundo

#########################################
#########################################
# Genero los datatypes date para iterar entre ellos y leo las carpetas
#########################################

print rcv_hms
print prs_hms

start_ymd = funciones.ymd(prs_year,prs_doy)
st_month  = start_ymd[1]
st_day    = start_ymd[2]
st_hour   = int(prs_hms[0:2])
st_min    = int(prs_hms[2:4])
st_scnd   = int(prs_hms[4:6])
starting_date = datetime(prs_year, st_month, st_day, st_hour, st_min, st_scnd)
# starting_date corresponde al ultimo archivo procesado, asi que incremento en un
# segundo para obtener el proximo posible. Si cambio de dia la operacion es correcta
starting_date += timedelta(seconds=1)

print starting_date 

ending_ymd = funciones.ymd(rcv_year,rcv_doy)
en_month   = ending_ymd[1]
en_day     = ending_ymd[2]
en_hour    = int(rcv_hms[0:2])
en_min     = int(rcv_hms[2:4])
en_scnd    = int(rcv_hms[4:6])
ending_date = datetime(rcv_year, en_month, en_day, en_hour, en_min, en_scnd)

# delta = timedelta(seconds=1)
# delta = timedelta(minutes=1)
delta = timedelta(days=1)
rango_fechas = funciones.datespan(starting_date, ending_date, delta)

# for f in rango_fechas:
#   print f

path_list = []

# iterar por mes o dia, listar los archivos, y de ahi filtrar los que cumplen el patron

for day in rango_fechas:

  # Path a los raw: day[0] = year, day[1] = month (completado con ceros hasta tener dos char)
  path_string = "/sat/raw-sat/" + str(day[0]) + "/" + str(day[1]).zfill(2) + "/"
  data_path   = os.path.abspath(path_string)

  # day[0] = year, day[2] = doy
  # el patron queda .*year\.doy.*\.nc
  # string_patron = ".*" + str(day[0]) + "\." + str(day[2]).zfill(3) + "\." + str(day[3]).zfill(2) + str(day[5]).zfill(2) + str(day[5]).zfill(2) + ".*" + "\.nc$"
  # string_patron = ".*" + str(day[0]) + "\." + str(day[2]).zfill(3) + "\." + str(day[3]).zfill(2) + str(day[5]).zfill(2) + ".*" + "\.nc$"
  string_patron = ".*" + str(day[0]) + "\." + str(day[2]).zfill(3) + ".*" + "\.nc$"
  pattern       = re.compile(string_patron)

  # listo solo los archivos del path elegido y que cumplen la expresion regular
  files_in_dir = [ path_string + f for f in listdir(data_path)
                   if isfile(join(data_path, f)) and pattern.match(f)
                 ] # for f in

  path_list.extend(files_in_dir)

# for day in rango_fechas 

for f in sorted(path_list):
  print f
