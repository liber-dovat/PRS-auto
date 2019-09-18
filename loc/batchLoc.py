#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import os
import glob
import sys
import numpy

from loc_types       import *
from os.path         import basename
from multiprocessing import Process, Manager
from threading       import Lock
from makeLoc         import calculateLoc
from funciones       import locValueArray2Array, locDateArray2Array, getCsvLocs, getIJArray

#########################################
#########################################
#########################################

CORES_DISPONIBLES = 30

if len(sys.argv) <= 1:
  print("Se nececitan los parámetros: path_base path_salida path_loc_file spatial_lat spatial_lon start_year end_year")
  raise SystemExit()

path_base     = sys.argv[1]
path_salida   = sys.argv[2]
path_loc_file = sys.argv[3]
spatial_lat   = float(sys.argv[4])
spatial_lon   = float(sys.argv[5])
start_year    = int(sys.argv[6])
end_year      = int(sys.argv[7])

mutex = Lock()

##################

# abro el archivo meta y guardo los datos
fid  = open(path_base + 'meta/' + 'T000gri.META', 'r')
meta = numpy.fromfile(fid, dtype='float32')
fid.close()

# abro el archivo T000gri.LATvec y guardo los datos
fid        = open(path_base + 'meta/' + 'T000gri.LATvec', 'r')
LATdeg_vec = numpy.fromfile(fid, dtype='float32')
LATdeg_vec = LATdeg_vec[::-1] # invierto el arreglo porque quedaba invertido verticalmente
fid.close()

# abro el archivo T000gri.LONvec y guardo los datos
fid        = open(path_base + 'meta/' + 'T000gri.LONvec', 'r')
LONdeg_vec = numpy.fromfile(fid, dtype='float32')
fid.close()

Ci = int(meta[0])
Cj = int(meta[1])

##################
##################

# cargar archivo de locs
locs_dic_csv   = getCsvLocs(path_loc_file)
locs_dic_coord = dict()

print('Calculando recortes')
for key in locs_dic_csv:
  print("Calculando %s"%key)
  value   = locs_dic_csv[key]
  loc_lat = value[0]
  loc_lon = value[1]
  coord_i, coord_j    = getIJArray(loc_lat, loc_lon, spatial_lat, spatial_lon, LATdeg_vec, LONdeg_vec)
  locs_dic_coord[key] = [loc_lat, loc_lon, coord_i, coord_j]

  if len(coord_i) == 0:
    print("LOC %s con tamaño 0"%key)

##################
##################

# si no existe, crar carpeta base (segun la resolucion) donde colocar los locs: T000loc_C01x01
resolution_basename = str(spatial_lat)[2:] + "x" + str(spatial_lon)[2:]
loc_prefix = "T000loc_C" + resolution_basename + "/"

path_salida_loc = path_salida + loc_prefix
os.makedirs(path_salida_loc, mode=0o775, exist_ok=True)

# Loop principal
for year in range(start_year, end_year+1):

  print("Año: " + str(year))

  locs_acumulado = dict()

  for key in locs_dic_coord:
    locs_acumulado[key] = Manager().list()

  locs_date = Manager().list()
  files     = []

  path_file    = path_base + 'B01-FR/'  + str(year) + "/"
  path_fileCNT = path_base + 'B01-CNT/' + str(year) + "/"

  files = sorted(glob.glob(path_file + "*.FR")) # for file in year
  files = list(map(basename,files))

  # files = files[0:4]

  print("Total archivos: %d" % (len(files)))

  while len(files) >= 1:

    print("Num files: %d" % (len(files)))

    processes = []

    # defino el total de procesos a lanzar por ves
    launch_proc = min(CORES_DISPONIBLES, len(files))

    for m in range(0, launch_proc):
      mutex.acquire() # mutoexcluyo para hacer el pop sin coliciones
      file = files.pop()
      mutex.release() # libero el mutex

      # array de datos de loc: coordenadas, resolucion
      # https://docs.python.org/2/library/multiprocessing.html
      parametros = [locs_date, path_file, file, path_fileCNT, locs_dic_coord, LATdeg_vec, LONdeg_vec, Ci, Cj, loc_res, launch_proc]

      # https://stackoverflow.com/questions/2046603/is-it-possible-to-run-function-in-a-subprocess-without-threading-or-writing-a-se

      p = Process(target=calculateLoc, args=(locs_acumulado, parametros))
      processes.append(p)
      p.start()
    # for

    # print("Num procesos: " + str(len(processes)))

    for p in processes:
      p.join()
      # print("Join proc")
    # for
    # print("End Join")

    del processes # vacío el array de procesos
  # end while

  print("Guardando locs " + str(year))
  for key in locs_acumulado:
    # print(key)
    locs_acumulado[key].sort()
    new_array_mean, new_array_msk, new_array_cnt = locValueArray2Array(locs_acumulado[key])
    loc_dir = path_salida_loc + key + "/"

    # si no exixte crar directorio del loc
    os.makedirs(loc_dir, mode=0o775, exist_ok=True)

    file_base_name = key + "_" + resolution_basename + "_" + str(year)

    # print("len(locs_acumulado[key]): %d"%(len(locs_acumulado[key])))

    # guardar arreglos dentro de la carpeta del loc, para cada a~no
    output_file = open(loc_dir + file_base_name + '.FR', 'wb')
    myarray = numpy.array(new_array_mean, dtype=numpy.float32)
    myarray.tofile(output_file)
    output_file.close()

    output_file = open(loc_dir + file_base_name + '.MSK', 'wb')
    myarray = numpy.array(new_array_msk, dtype=numpy.int16)
    myarray.tofile(output_file)
    output_file.close()

    output_file = open(loc_dir + file_base_name + '.CNT', 'wb')
    myarray = numpy.array(new_array_cnt, dtype=numpy.int16)
    myarray.tofile(output_file)
    output_file.close()

  # for key end

  # guardar date por año, todos en la carpeta base de locs
  locs_date.sort()
  print("len(locs_date): %d"%(len(locs_date)))
  locs_date_array = locDateArray2Array(locs_date)
  date_base_name = "C" + resolution_basename + "_" + str(year)

  print("guardando año " + str(year))
  output_file = open(path_salida_loc + date_base_name + '.DATE', 'wb')
  myarray = numpy.array(locs_date_array, dtype=numpy.float32)
  myarray.tofile(output_file)
  output_file.close()

  del files
  del locs_acumulado
  del locs_date

# end for year
