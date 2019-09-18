#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import numpy
import datetime
from loc_types import *

from os.path         import basename
from funciones       import cosSolarZenithAngle

#########################################
#########################################
#########################################

def getDate(file):

  base_file = basename(file)
  year      = base_file[4:8]
  doy       = base_file[8:11]
  hh        = base_file[12:14]
  mm        = base_file[14:16]
  ss        = base_file[16:18]

  return int(year), int(doy), int(hh), int(mm), int(ss)

#########################################
#########################################
#########################################

def calculateLoc(locs_acumulado, parameters):

  # print(parameters)
  locs_date      = parameters[0]
  path_file      = parameters[1]
  file           = parameters[2]
  path_fileCNT   = parameters[3]
  locs_dic_coord = parameters[4]
  LATdeg_vec     = parameters[5]
  LONdeg_vec     = parameters[6]
  Ci             = int(parameters[7])
  Cj             = int(parameters[8])

  Ct = Ci*Cj

  ##############################

  epoch = datetime.datetime.strptime('2000 01 00 00 00', '%Y %j %H %M %S')

  # file = abrir archivo
  fid  = open(path_file + file, 'r')
  data = numpy.fromfile(fid, dtype='float32') # FR
  fid.close()

  IMG = []
  IMG = numpy.reshape(data, (Ci, Cj))

  # MSK
  fileCNT = file[:-2] + "CNT"
  fid     = open(path_fileCNT + fileCNT, 'r')
  dataCNT = numpy.fromfile(fid, dtype='int16') # CNT
  fid.close()

  CNT = []
  CNT = numpy.reshape(dataCNT, (Ci, Cj))

  ### Date
  year, doy, hh, mm, ss = getDate(file)

  time_data = str(year) + " " + str(doy) + " " + str(hh)  + " " + str(mm)  + " " + str(ss)
  date      = datetime.datetime.strptime(time_data, '%Y %j %H %M %S')

  ite = float((date-epoch).total_seconds())/(24.0*60.0*60.0) # segundos desde el 2000-01-00:00:00 dividido total de secs en un dia

  date_value = DateType(year, doy, hh, mm, ss, ite)
  locs_date.append(date_value)

  # para cada loc calcular el recorte, el mean
  for loc in locs_dic_coord:

    loc_data = locs_dic_coord[loc]

    loc_lat = loc_data[0]
    loc_lon = loc_data[1]
    coord_i = loc_data[2]
    coord_j = loc_data[3]

    mean  = 0.0
    cnt   = 0.0
    ERROR = False

    try:
      IMG_small = IMG[coord_i,coord_j]
      CNT_small = CNT[coord_i,coord_j]

      if len(IMG_small) != 0:
        mean = numpy.mean(IMG_small)
        cnt  = numpy.sum(CNT_small)
      # else:
      #   print(numpy.shape(IMG_small))
      #  print("CNT: %d"%cnt)

    except OSError as err:
      # print("OS error: {0}".format(err))
      ERROR = True
    except ValueError:
      # print("Could not convert data to an integer.")
      ERROR = True
    except:
      # print("Unexpected error:", sys.exc_info()[0])
      raise

    csza = cosSolarZenithAngle(loc_lat, loc_lon, date)

    if (mean>0) or (csza<=0) or not ERROR:
      msk = 1
    else:
      msk = 0

    # Uso el array pasado como parametro para cargar los datos y encolar al final
    type_value = LocType(mean, msk, cnt, ite)
    locs_acumulado[loc].append(type_value)

    del IMG_small

  # for loc end

# calculateLoc()
