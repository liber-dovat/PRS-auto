#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import subprocess

from file_to_png import fileToPng
from shutil      import copyfile
from funciones   import copiar_frames, makeTimestamp, getYearRootBand

PATHpng = '/sat/prd-sat/PNGs/'

baseVIS = '/sat/prd-sat/ART_G015x015GG_C015x015/'

meta15  = baseVIS + 'meta/'

# abro el archivo cuya ruta es el primer parametro
# debe ser el archivo job_imglist_VIS1
# lista = open(sys.argv[1], 'r')

# abro el archivo y remuevo las lineas vacias
lista = filter(None, (line.rstrip() for line in open(sys.argv[1], 'r')))

for f in lista:

  year, rootname, band = getYearRootBand(f)

  FRpath  = baseVIS + 'B01-FR/' + year + '/' + rootname + '.FR'
  RPpath  = baseVIS + 'B01-RP/' + year + '/' + rootname + '.RP'

  fileToPng(FRpath,  meta15, PATHpng)
  fileToPng(RPpath,  meta15, PATHpng)

  # si es el ultimo archivo procesado
  # y ya estan procesados los archivos de IRB
  if f == lista[-1] and os.path.isfile(PATHpng + 'B06/' + year + '/' + rootname + '.png'):

    # genero una copia de cada imagen para subir a la web
    fileFR = PATHpng + 'B01-FR/' + year + '/' + rootname + '.png'
    fileRP = PATHpng + 'B01-RP/' + year + '/' + rootname + '.png'

    copyfile(fileFR, PATHpng + "BAND_01-FR.png")
    copyfile(fileRP, PATHpng + "BAND_01-RP.png")

    subprocess.call("/sat/PRS/libs/PRS-auto/PRSpost/rmframes.sh", shell=True)
    copiar_frames(PATHpng + 'B01-FR/' + year, PATHpng + 'B01-FR/mp4')
    copiar_frames(PATHpng + 'B01-RP/' + year, PATHpng + 'B01-RP/mp4')

    timestamp = makeTimestamp(year, rootname)

    timestamp_file = open(PATHpng + 'timestamp.html', 'w')
    timestamp_file.write(timestamp)
    timestamp_file.close()

    subprocess.call("/sat/PRS/libs/PRS-auto/PRSpost/videoandcopy.sh", shell=True)
  # if

# if