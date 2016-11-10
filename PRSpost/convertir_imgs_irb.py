#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import subprocess

from file_to_png import fileToPng
from shutil      import copyfile
from funciones   import copiar_frames, makeTimestamp, getYearRoot

PATHpng = '/sat/prd-sat/PNGs/'

baseIR  = '/sat/prd-sat/ART_G060x060GG_C060x060/'

meta60  = baseIR + 'meta/'

# abro el archivo cuya ruta es el primer parametro
# debe ser el archivo job_imglist_IRB1
# lista = open(sys.argv[1], 'r')

# abro el archivo y remuevo las lineas vacias
lista = filter(None, (line.rstrip() for line in open(sys.argv[1], 'r')))

for f in lista:

  year, rootname = getYearRoot(f)

  B02path = baseIR  + 'B02-T2/' + year + '/' + rootname + '.T2'
  B03path = baseIR  + 'B03-T3/' + year + '/' + rootname + '.T3'
  B04path = baseIR  + 'B04-T4/' + year + '/' + rootname + '.T4'
  B06path = baseIR  + 'B06-T6/' + year + '/' + rootname + '.T6'

  fileToPng(B02path, meta60, PATHpng)
  fileToPng(B03path, meta60, PATHpng)
  fileToPng(B04path, meta60, PATHpng)
  fileToPng(B06path, meta60, PATHpng)

  # si es el ultimo archivo procesado
  # y ya estan procesados los archivos de VIS
  if f == lista[-1] and os.path.isfile(PATHpng + 'B01-RP/' + year + '/' + rootname + '.png'):

    fileB02 = PATHpng + 'B02/' + year + '/' + rootname + '.png'
    fileB03 = PATHpng + 'B03/' + year + '/' + rootname + '.png'
    fileB04 = PATHpng + 'B04/' + year + '/' + rootname + '.png'
    fileB06 = PATHpng + 'B06/' + year + '/' + rootname + '.png'

    copyfile(fileB02, PATHpng + "BAND_02.png")
    copyfile(fileB03, PATHpng + "BAND_03.png")
    copyfile(fileB04, PATHpng + "BAND_04.png")
    copyfile(fileB06, PATHpng + "BAND_06.png")

    subprocess.call("/sat/PRS/libs/PRS-auto/PRSpost/rmframes.sh", shell=True)
    copiar_frames(PATHpng + 'B04/' + year, PATHpng + 'B04/mp4')

    timestamp = makeTimestamp(year, rootname)

    timestamp_file = open(PATHpng + 'timestamp.html', 'w')
    timestamp_file.write(timestamp)
    timestamp_file.close()

    subprocess.call("/sat/PRS/libs/PRS-auto/PRSpost/videoandcopy.sh", shell=True)
  # if

# if