#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import glob
import sys

from os.path         import isfile, basename
from os              import listdir
from multiprocessing import Process
from threading       import Lock
from funciones       import llamarScript, readFolders, readSpatial, generar_grilla, guardar_grilla, cargar_calibracion_VIS

#########################################
#########################################
#########################################

if len(sys.argv) <= 1:
  print("Se nececitan los parámetros: start_month start_year end_month end_year")
  raise SystemExit()

start_month = int(sys.argv[1])
start_year  = int(sys.argv[2])
end_month   = int(sys.argv[3])
end_year    = int(sys.argv[4])

print(start_month)
print(start_year)
print(end_month)
print(end_year)

programa = '/solar/sat/PRS/dev/PRS-sat/PRSGoesRMultiproc/PRS_auto_R'

RUTAent, RUTAbase, RUTAcal =\
readFolders('/solar/sat/PRS/dev/PRS-sat/PRSGoesRMultiproc/data/job_folders_ALL1')

LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, dLATcel, dLONcel, CODEspatial =\
readSpatial('/solar/sat/PRS/dev/PRS-sat/PRSGoesRMultiproc/data/job_spatial_VIS1')

RUTAsal = RUTAbase + CODEspatial + "/"
print(RUTAsal)

os.makedirs(RUTAsal + 'meta/', mode=0o777, exist_ok=True)
os.makedirs(RUTAsal + 'test/', mode=0o777, exist_ok=True)
os.makedirs(RUTAsal + 'zCRR/', mode=0o777, exist_ok=True)

# Generar y guardar la grilla se ejecutan una vez sola al principio de la corrida
LATmat, LONmat, LATvec, LONvec, Ci, Cj, Ct =\
generar_grilla(LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri)
guardar_grilla(RUTAsal, Ci, Cj, LATmax, dLATgri, LONmin, dLONgri, LATvec, LONvec, LATmat, LONmat)

# PRODUCTOS
product = ['B02-FR/', 'B02-MK/', 'B02-CNT/']

mutex = Lock()

# Loop principal
for year in range(start_year, end_year+1):

  print("Año: " + str(year))

  for prod in product:
    os.makedirs(RUTAsal + prod + str(year), mode=0o777, exist_ok=True)
    os.makedirs(RUTAsal + "zIMP/" + prod + str(year), mode=0o777, exist_ok=True)

  # pasar las calibraciones por párametro
  # se determina la calibración en función del satélite
 
  start_m = 1
  end_m   = 12

  if year == start_year:
    start_m = start_month
  
  if year == end_year:
    end_m = end_month
  # end if

  files = []

  for month in range(start_m, end_m+1):

    print("Mes: " + str(month))

    path = RUTAent + str(year) + "/" + str(month).zfill(2) + "/C02/"

    files = sorted(glob.glob(path+"/*G16*.nc"))
    files = list(map(basename,files))

    while len(files)>=1:

      print("Num files: " + str(len(files)))

      processes = []

      numproc = 1
      if len(files) < numproc:
        numproc = len(files)

      for m in range(0, numproc):
        mutex.acquire() # mutoexcluyo para hacer el pop sin coliciones
        file = files.pop()
        mutex.release() # libero el mutex

        parametros =path         + " " +\
                    RUTAsal      + " " +\
                    file         + " " +\
                    str(LATmax)  + " " +\
                    str(LATmin)  + " " +\
                    str(LONmax)  + " " +\
                    str(LONmin)  + " " +\
                    str(dLATgri) + " " +\
                    str(dLONgri) + " " +\
                    str(dLATcel) + " " +\
                    str(dLONcel) + " " +\
                    str(Ci)      + " " +\
                    str(Cj)      + " " +\
                    str(Ct)      + " " +\
                    CODEspatial

        # print(parametros)

        p = Process(target=llamarScript, args=(programa, parametros))
        p.start()
        processes.append(p)
      # for

      print("Num procesos: " + str(len(processes)))

      for p in processes:
        p.join()
      # for

      del processes # vacío el array de procesos

    # end while

  # end for month

  del files # vacío el array de archivos

# end for year
