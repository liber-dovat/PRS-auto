# Funciones copiadas de:
# http://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python

import calendar
from datetime import date, datetime
from os       import listdir, remove
from shutil   import copyfile

def doy(Y,M,D):
  """ given year, month, day return day of year
      Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """
  if calendar.isleap(Y):
      K = 1
  else:
      K = 2
  N = int((275 * M) / 9.0) - K * int((M + 9) / 12.0) + D - 30
  return N

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

def ymd(Y,N):
  """ given year = Y and day of year = N, return year, month, day
      Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """    
  if calendar.isleap(Y):
      K = 1
  else:
      K = 2
  M = int((9 * (K + N)) / 275.0 + 0.98)
  if N < 32:
      M = 1
  D = N - int((275 * M) / 9.0) + K * int((M + 9) / 12.0) + 30
  return Y, M, D

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# http://stackoverflow.com/questions/5734438/how-to-create-a-month-iterator
# Iterador de meses

def months(start_month, start_year, end_month, end_year):
  month, year = start_month, start_year
  while True:
    yield month, year
    if (month, year) == (end_month, end_year):
        return  
    month += 1
    if (month > 12):
        month = 1
        year += 1

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# http://stackoverflow.com/questions/153584/how-to-iterate-over-a-timespan-after-days-hours-weeks-and-months-in-python

def datespan(startDate, endDate, delta):
  
  # C = currentDate
  C = startDate
  while C <= endDate:
    yield C.year, C.month, doy(C.year, C.month, C.day), C.hour, C.minute, C.second 
    C += delta

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

def getLastFile(basedir):

  year     = sorted(listdir(basedir))[-1]
  rootname = sorted(listdir(basedir + year + '/'))[-1]

  return year, rootname[:18]

# getLastFileFRPath

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

def copiar_frames(carpeta_base, carpeta_destino):

  # habia usado 92 elems en las pruebas que eran cerca de tres dias
  # tambien se puede pensar que son 44 por dia

  dir_elemens = sorted(listdir(carpeta_base))
  indice      = 88
  if len(dir_elemens) < 88:
    indice = len(dir_elemens)

  ultimas = dir_elemens[-indice:]

  i = 0

  for f in ultimas:
    copyfile(carpeta_base + '/' + f, carpeta_destino + '/' + f)
    i += 1

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

'''
borra el primer frame de la carpeta, y copia el ultimo frame
de la carpeta de procesados
'''

def actualizarFrames(carpeta_base, carpeta_destino):

  # borro el primer frame de la carpeta de procesados
  primero = sorted(listdir(carpeta_destino))[0]
  remove(carpeta_destino + '/' + primero)

  # obtengo el ultimo elemento de la carpeta de procesados y lo copio en frames
  ultima = sorted(listdir(carpeta_base))[-1]
  copyfile(carpeta_base + '/' + ultima, carpeta_destino + '/' + ultima)

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

'''
Convertir 2016/10/goes13.2016.275.143506.BAND_02.nc
a         2016 y ART_2016275_143506
'''

def getYearRoot(basedir):
  year     = basedir.split('/')[0]
  name     = basedir.split('/')[2].split('.')
  rootname = "ART_" + name[1] + name[2] + "_" + name[3]

  return year, rootname

# getYearRoot

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

'''
Genero un string de timestamp a partir del ano y el nombre base del archivo
'''

def makeTimestamp(year, rootname):

  doy       = rootname[8:11]                  # obtengo el doy del rootname
  hms       = rootname[12:18]                 # obtengo la hora minuto y segundo del rootname
  month     = ymd(int(year), int(doy))[1]     # obtengo el mes usando la funcion ymd
  timestamp = year + '.' + str(month).zfill(2) + '.' + str(doy).zfill(3) + '.' + hms

  return timestamp

# makeTimestamp