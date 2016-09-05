#!/usr/bin/python

# importo el modulo funciones
import funciones
from datetime import date

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

rcv_month = int(rcv_split[1]) # la segunda palabra del arreglo es el mes
prs_month = int(prs_split[1]) # la segunda palabra del arreglo es el mes

rcv_doy = int(rcv_split[2]) # la tercera palabra del arreglo es el doy
prs_doy = int(prs_split[2]) # la tercera palabra del arreglo es el doy

print rcv_year
print prs_year
print str(rcv_month).zfill(2) # lleno con ceros el integer correspondiente al numero
print str(prs_month).zfill(2) # lleno con ceros el integer correspondiente al numero
print rcv_doy
print prs_doy

years = []
for y in range(int(prs_split[0]), int(rcv_split[0])+1):
  years.append(y)

  # Returns weekday of first day of the month and number of days in month, for the specified year and month.
  # calendar.monthrange(year, month)

# doy = yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1

print years

start_ymd = funciones.ymd(prs_year,prs_doy)
starting_year  = prs_year
starting_month = start_ymd[1]
starting_day   = start_ymd[2] + 1
starting_doy   = prs_doy - starting_day
starting_date  = date(starting_year, starting_month,starting_day)

ending_ymd = funciones.ymd(rcv_year,rcv_doy)
ending_year  = rcv_year
ending_month = ending_ymd[1]
ending_day   = ending_ymd[2]
ending_doy   = rcv_doy - ending_day
ending_date  = date(ending_year, ending_month, ending_day)

print starting_year
print starting_month
print starting_doy

for day in funciones.datespan(starting_date, ending_date):
  print day

# rcv_split[1] y prs_split[1] es el ano
# si prs[ano] es menor estricto que rcv[ano]
#   genero los anos que faltan entre medio
#   desde prs[ano] hasta rcv[ano] voy metiendo los valores en un arreglo
#   pj prs[ano]=2011, rcv[ano]=2015, anos = [2011, 2012, 2013, 2014, 2015]

# Luego repito para el mes

# y por ultimo hago un for doble anidado, por ano y mes, para generar los paths

# luego, para cada path ...

pattern = re.compile(".*prs.*")

# listo solo los archivos del path elegido y que cumplen la expresion regular
files_in_dir = [f for f in listdir(abs_file_path)
                 if isfile(join(abs_file_path, f)) and
                 pattern.match(f)
               ] # for f in

print files_in_dir

