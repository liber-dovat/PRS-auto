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

subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/imgcopy.sh", shell=True)
