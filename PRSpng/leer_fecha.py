#!/usr/bin/python

# importo el modulo funciones y dateime
from funciones import ymd
from netcdfio  import netcdf2png
# importo rutinas para trabajar con el sistema operativo
import os
from   os      import listdir
from   os.path import isfile, join, basename
from   shutil  import copyfile

# importo rutinas de expresiones regulares
import re

def getDateArray():
  #########################################
  #########################################
  # Defino las rutas a los archivos para poder trabajar con ellos
  #########################################

  # genero los paths para los directorios base
  data_path     = "/sat/PRS/libs/PRS-auto/data/"
  abs_file_path = os.path.abspath(data_path)

  # declaro los paths para los dos archivos
  prs_path = os.path.join(abs_file_path, 'last-image-prs')
  rcv_path = os.path.join(abs_file_path, 'last-image-rcv')

  # abro los dos archivos para trabajar con ellos
  # el primero es de solo lectura, y el segundo es de lectura escritura
  ultima_procesada = open(prs_path, 'r')
  ultima_recibida  = open(rcv_path, 'r+')

  #########################################
  #########################################
  # Recorro las lineas de los documentos y las imprimo
  #########################################

  # para cada linea del archivo, la imprimo
  for line in ultima_procesada:
    # tomo la linea y genero un arreglo con sus palabras
    prs_split = line.split(".")
  # for

  # para cada linea del archivo, la imprimo
  for line in ultima_recibida:
    # tomo la linea y genero un arreglo con sus palabras
    rcv_split = line.split(".")
  # for

  ultima_procesada.close()
  ultima_recibida.close()

  #########################################
  #########################################
  # Realizo operaciones de impresion en pantalla para ver los parametros
  #########################################

  prs_year  = int(prs_split[0]) # la primer palabra del arreglo es el ano
  prs_month = int(prs_split[1]) # la segunda palabra del arreglo es el mes
  prs_doy   = int(prs_split[2]) # la tercera palabra del arreglo es el doy
  prs_hms   = prs_split[3]      # la cuarta palabra del arreglo es la hora-minuto-segundo

  st_hour   = int(prs_hms[0:2])
  st_min    = int(prs_hms[2:4])
  st_scnd   = int(prs_hms[4:6])

  rcv_year  = int(rcv_split[0]) # la primer palabra del arreglo es el ano
  rcv_month = int(rcv_split[1]) # la segunda palabra del arreglo es el mes
  rcv_doy   = int(rcv_split[2]) # la tercera palabra del arreglo es el doy
  rcv_hms   = rcv_split[3]      # la cuarta palabra del arreglo es la hora-minuto-segundo

  en_hour   = int(rcv_hms[0:2])
  en_min    = int(rcv_hms[2:4])
  en_scnd   = int(rcv_hms[4:6])

  #########################################
  #########################################
  # Genero los datatypes date para iterar entre ellos y leo las carpetas
  #########################################

  # genero los numeros enteros para realizar el chequeo de archivos que quiero
  #                 ano                mes            doy            hora+minuto+segundo
  start_timestamp = int(prs_split[0] + prs_split[1] + prs_split[2] + prs_hms)
  end_timestamp   = int(rcv_split[0] + rcv_split[1] + rcv_split[2] + rcv_hms)

  path_list = []

  # hago un doble for de anos y meses
  # los anos iteran desde el primero hasta el ultimo
  # range no considera el ultimo elemento en el rango, por eso para incluirlo usamos el +1
  for year in range(prs_year, rcv_year + 1):

    primer_mes = 1
    ultimo_mes = 12

    # para el primer ano solo debo iterar desde el mes del archivo
    # y para el ultimo ano solo debo iterar hasta el mes del archivo
    if year == prs_year:
      primer_mes = prs_month
    # if

    if year == rcv_year:
      ultimo_mes = rcv_month
    # if

    # range no considera el ultimo elemento en el rango, por eso para incluirlo usamos el +1
    for month in range(primer_mes, ultimo_mes + 1):

      # Path a los raw: day[0] = year, day[1] = month (completado con ceros hasta tener dos char)
      path_string = "/sat/raw-sat/" + str(year) + "/" + str(month).zfill(2) + "/"
      data_path   = os.path.abspath(path_string)

      # day[0] = year, day[2] = doy
      # el patron queda .*year\.doy.*\.nc
      string_patron = ".*" + str(year) + "\." + ".*" + "\.nc$"
      pattern       = re.compile(string_patron)

      for f in listdir(data_path):
        if isfile(join(data_path, f)) and pattern.match(f):
          nombre  = f.split(".") # separo el nombre del archivo en palabras separadas
          ano     = nombre[1]
          doy     = nombre[2]
          hms     = nombre[3]

          mes     = ymd(int(ano),int(doy))[1] # convierto ano y doy a ano mes y dia, y me quedo con el mes
          mes_str = str(mes).zfill(2) # lo convierto a string y lo relleno de ceros en el frente

          # genero su timestamp a partir de su nombre
          timestamp = int( ano + mes_str + doy + hms )

          # si el timestamp esta dentro de los rangos definidos por los archivos lo agrego a la lista
          if timestamp > start_timestamp and timestamp <= end_timestamp:
            path_list.extend([data_path + "/" + f])
          # if

        # if
      # for

    # for month

  # for year

  lista_retorno = sorted(path_list)

  # escribo en archivo rcv_path la fecha de la ultima imagen recibida
  if len(lista_retorno) > 0:
    ultimo_elem   = lista_retorno[-1]
    elemen_split  = ultimo_elem.split(".")[1:4]
    month         = ymd(int(elemen_split[0]), int(elemen_split[1]))
    elemen_split.insert(1, str(month[1]).zfill(2))
    ultima_recibida = open(rcv_path, 'w')
    ultima_recibida.write(elemen_split[0]+'.'+elemen_split[1]+'.'+elemen_split[2]+'.'+elemen_split[3]+'\n')
    ultima_recibida.close()

  return lista_retorno

# getDateArray

def lastReceived():

  path = "/sat/raw-sat/"

  years  = sorted(os.listdir(path))

  if len(years) > 0:
    path  += years[-1] + "/"
    months = sorted(os.listdir(path))

    if len(months) > 0:
      path  += months[-1] + "/"
      files = sorted(os.listdir(path))

      if len(files) > 0:

        file = files[-1]
        name_split = file.split(".")
        name_split = name_split[1:4]
        month = ymd(int(name_split[0]), int(name_split[1]))
        name_split.insert(1, str(month[1]).zfill(2))

        # genero los paths para los directorios base
        data_path     = "/sat/PRS/libs/PRS-auto/data/"
        abs_file_path = os.path.abspath(data_path)

        # declaro los paths para los dos archivos
        rcv_path = os.path.join(abs_file_path, 'last-image-rcv')

        # abro el archivo
        ultima_recibida = open(rcv_path, 'w')
        ultima_recibida.write(name_split[0]+'.'+name_split[1]+'.'+name_split[2]+'.'+name_split[3]+'\n')

# lastReceived

lastReceived()
arreglo = getDateArray()

for file in arreglo:

  print file
  netcdf2png(file,'/sat/PRS/libs/PRS-auto/PRSpng/png/')

  if file == arreglo[-1]:
    filename   = basename(file)
    name_split = filename.split(".")
    name_split = name_split[1:4]
    # print name_split
    month = ymd(int(name_split[0]), int(name_split[1]))
    name_split.insert(1, str(month[1]).zfill(2))
    # print name_split[0]+'.'+name_split[1]+'.'+name_split[2]+'.'+name_split[3]+'\n'

    # genero los paths para los directorios base
    data_path     = "/sat/PRS/libs/PRS-auto/data/"
    abs_file_path = os.path.abspath(data_path)

    # declaro los paths para los dos archivos
    prs_path = os.path.join(abs_file_path, 'last-image-prs')

    # abro los dos archivos para trabajar con ellos
    # el primero es de solo lectura, y el segundo es de lectura escritura
    ultima_procesada = open(prs_path, 'w')
    ultima_procesada.write(name_split[0]+'.'+name_split[1]+'.'+name_split[2]+'.'+name_split[3]+'\n')

  # BAND_01
  root = "/sat/PRS/libs/PRS-auto/PRSpng/png/"

  if file == arreglo[-5]:
      pattern = re.compile(".*BAND_01\.nc$")
      if pattern.match(file):
        copyfile(root + basename(file) + ".png", root + "BAND_01.png")
  elif file == arreglo[-4]:
      pattern = re.compile(".*BAND_02\.nc$")
      if pattern.match(file):
        copyfile(root + basename(file) + ".png", root + "BAND_02.png")
  elif file == arreglo[-3]:
      pattern = re.compile(".*BAND_03\.nc$")
      if pattern.match(file):
        copyfile(root + basename(file) + ".png", root + "BAND_03.png")
  elif file == arreglo[-2]:
      pattern = re.compile(".*BAND_04\.nc$")
      if pattern.match(file):
        copyfile(root + basename(file) + ".png", root + "BAND_04.png")
  elif file == arreglo[-1]:
      pattern = re.compile(".*BAND_06\.nc$")
      if pattern.match(file):
        copyfile(root + basename(file) + ".png", root + "BAND_06.png")
