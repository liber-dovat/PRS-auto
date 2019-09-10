#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import subprocess
from netcdfio_irradiancia import netcdf2png, ncdump
from utils import copiar_frames

ncpath   = '/sat/PRS/dev/PRS-sat/PRSgoes/tmp/'
dirDest  = '/sat/prd-sat/PNGs/'
cmapPath = '/sat/PRS/dev/PRS-sat/PRSgoes/cmaps/'

# sincronizo los archivos para procesar
# subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/descargar_tmp.sh", shell=True)

files = ['band13.nc']

tmp = 'none'

timestamp = ""

for i in files:
  file = ncpath + i
  # ncdump(file)
  if i == 'band13.nc':
    cmap = 'cptec2'
  else:
    cmap = 'jet'
  
  tmp = netcdf2png(file, cmapPath, cmap, dirDest, 'y', 'x','CMI')

  if i == 'band02.nc':
    timestamp = tmp

print(timestamp)
timestamp_html = open(dirDest + 'timestamp.html', 'w')
timestamp_html.write(timestamp)
timestamp_html.close()

subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/imgcopy.sh", shell=True)
