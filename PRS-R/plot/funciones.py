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
  indice      = 44
  if len(dir_elemens) < 44:
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

def getYearRootBand(basedir):
  year     = basedir.split('/')[0]
  name     = basedir.split('/')[2].split('.')
  rootname = "ART_" + name[1] + name[2] + "_" + name[3]
  banda    = name[4]

  if banda == "BAND_02":
    band = "B02-T2"
  elif banda == "BAND_03":
    band = "B03-T3"
  elif banda == "BAND_04":
    band = "B04-T4"
  elif banda == "BAND_06":
    band = "B06-T6"

  return year, rootname, band

# getYearRoot

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

'''
ART_2016275_143506
'''

def getRootnameYear(rootname):
  nombre = rootname.split("_") # separo el nombre del archivo en palabras separadas
  year   = nombre[1][0:4]

  return year

# getRootnameYear

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

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

'''
Escribo en el archivo /sat/PRS/libs/PRS-sat/data/last-image-rcv el patron
de la ultima imagen recibida
'''

def lastReceived(file_path, rcv_path):

  years = sorted(listdir(file_path))

  if len(years) > 0:
    file_path  += years[-1] + "/"

    files = sorted(listdir(file_path))

    # ART_2016316_143800.FR
    if len(files) > 0:

      file = files[-1]
      basename = file.split(".")[0]

      ultima_recibida = open(rcv_path, 'w')
      ultima_recibida.write(basename)

    # if

# lastReceived

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

'''
retorna una lista de elementos con el siguiente formato: ART_2016316_140800
'''

def getDateArray(prs_path, rcv_path, file_path):

  # abro los dos archivos para trabajar con ellos
  # el primero es de solo lectura, y el segundo es de lectura escritura
  prs = open(prs_path, 'r')
  rcv = open(rcv_path, 'r+')

  #########################################
  #########################################
  # Recorro las lineas de los documentos y las imprimo
  #########################################

  # tomo la linea y genero un arreglo con sus palabras
  prs_read = prs.read()
  prs_split = prs_read.split("_")

  # tomo la linea y genero un arreglo con sus palabras
  rcv_read = rcv.read()
  rcv_split = rcv_read.split("_")

  prs.close()
  rcv.close()

  #########################################
  #########################################

  prs_year  = prs_split[1][0:4]
  prs_doy   = prs_split[1][4:7]
  prs_hms   = prs_split[2]

  rcv_year  = rcv_split[1][0:4]
  rcv_doy   = rcv_split[1][4:7]
  rcv_hms   = rcv_split[2]

  #########################################
  #########################################
  # Genero los datatypes date para iterar entre ellos y leo las carpetas
  #########################################

  # genero los numeros enteros para realizar el chequeo de archivos que quiero
  #                 ano                mes            doy            hora+minuto+segundo
  start_timestamp = int(prs_year + prs_doy + prs_hms)
  end_timestamp   = int(rcv_year + rcv_doy + rcv_hms)

  print start_timestamp
  print end_timestamp

  files_list = []

  # hago un doble for de anos y meses
  # los anos iteran desde el primero hasta el ultimo
  # range no considera el ultimo elemento en el rango, por eso para incluirlo usamos el +1
  for year in range(int(prs_year), int(rcv_year) + 1):

    # Path a los raw: day[0] = year, day[1] = month (completado con ceros hasta tener dos char)
    path_string = file_path + str(year) + "/"

    for f in listdir(path_string):

      tmp_nm  = f.split(".")[0]
      nombre  = tmp_nm.split("_") # separo el nombre del archivo en palabras separadas
      ano     = nombre[1][0:4]
      doy     = nombre[1][4:7]
      hms     = nombre[2]

      # genero su timestamp a partir de su nombre
      timestamp = int(ano + doy + hms)

      # si el timestamp esta dentro de los rangos definidos por los archivos lo agrego a la lista
      if timestamp > start_timestamp and timestamp <= end_timestamp:
        files_list.extend([f[0:18]])
      # if

    # for

  # for year

  lista_retorno = sorted(files_list)

  # escribo en archivo rcv_path la fecha de la ultima imagen recibida
  if len(lista_retorno) > 0:
    ultimo_elem     = lista_retorno[-1]

    ultima_recibida = open(rcv_path, 'w')
    ultima_recibida.write(ultimo_elem)
    ultima_recibida.close()
  # if

  print lista_retorno

  return lista_retorno

# getDateArray
