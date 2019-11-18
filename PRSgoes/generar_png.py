#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import subprocess
import datetime
from netcdfio import fr2png, ncdump
from netcdfio_irr import fr2ghi2png
from utils import copiar_frames

ncpath   = '/sat/PRS/dev/PRS-sat/PRSgoes/tmp/'
dirDest  = '/sat/prd-sat/PNGs/'
cmapPath = '/sat/PRS/dev/PRS-sat/PRSgoes/cmaps/'

# sincronizo los archivos para procesar
subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/descargar_tmp.sh", shell=True)

files = ['band02.nc','band13.nc']

tmp = 'none'

timestamp = ""

for i in files:
  file = ncpath + i
  # ncdump(file)
  if i == 'band13.nc':
    cmap = 'cptec2'
  else:
    cmap = 'jet'
  
  tmp = fr2png(file, cmapPath, cmap, dirDest, 'y', 'x','CMI')

  if i == 'band02.nc':
    timestamp = tmp

fr2ghi2png(ncpath + 'band02_uy.nc', cmapPath, cmap, dirDest, 'y', 'x','CMI')

print(timestamp)
timestamp_html = open(dirDest + 'timestamp.html', 'w')
timestamp_html.write(timestamp)
timestamp_html.close()

# borro los frames de los videos para generarlos de nuevo
subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/rmframes.sh", shell=True)

# copio los frames que voy a usar para generar los videos
# en función del nombre de las imagenes genero el timestamp
# luego llamo a videoandcopy para generar los videos y copiar todo a la web

year = str(datetime.datetime.now().year)

print('copio los frames')
copiar_frames(dirDest + 'C02/' + year, dirDest + 'C02/mp4')
copiar_frames(dirDest + 'C13/' + year, dirDest + 'C13/mp4')

# subprocess.call(["ls", "-l"])

subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/videoandcopy.sh", shell=True)
