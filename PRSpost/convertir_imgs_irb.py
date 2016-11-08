#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from file_to_png import fileToPng
from shutil      import copyfile
from funciones   import ymd, getLastFile, copiar_frames

PATHpng = '/sat/prd-sat/PNGs/'

baseIR  = '/sat/prd-sat/ART_G060x060GG_C060x060/'

meta60  = baseIR  + 'meta/'

# /sat/PRS/libs/PRS-auto/data/job_imglist_IRB1

lista = open(sys.argv[1], 'r')

for f in lista:

  year, rootname = getYearRoot(f)

  print year
  print rootname

  B02path = baseIR  + 'B02-T2/' + year + '/' + rootname + '.T2'
  B03path = baseIR  + 'B03-T3/' + year + '/' + rootname + '.T3'
  B04path = baseIR  + 'B04-T4/' + year + '/' + rootname + '.T4'
  B06path = baseIR  + 'B06-T6/' + year + '/' + rootname + '.T6'

  fileToPng(B02path, meta60, PATHpng)
  fileToPng(B03path, meta60, PATHpng)
  fileToPng(B04path, meta60, PATHpng)
  fileToPng(B06path, meta60, PATHpng)

  # si es el ultimo archivo procesado
  if f == lista[-1]:

    file = PATHpng + 'B02/' + year + '/' + rootname + '.png'
    copyfile(file, PATHpng + "BAND_02.png")

    file = PATHpng + 'B03/' + year + '/' + rootname + '.png'
    copyfile(file, PATHpng + "BAND_03.png")

    file = PATHpng + 'B04/' + year + '/' + rootname + '.png'
    copyfile(file, PATHpng + "BAND_04.png")

    file = PATHpng + 'B06/' + year + '/' + rootname + '.png'
    copyfile(file, PATHpng + "BAND_06.png")

    copiar_frames(PATHpng + 'B04/' + year, PATHpng + 'B04/mp4')

    doy   = rootname[8:11]                  # obtengo el doy del rootname
    hms   = rootname[12:18]                 # obtengo la hora minuto y segundo del rootname
    month = ymd(int(year), int(doy))[1]     # obtengo el mes usando la funcion ymd
    timestamp = year + '.' + str(month).zfill(2) + '.' + str(doy).zfill(3) + '.' + hms

    timestamp_file = open(PATHpng + 'timestamp.html', 'w')
    timestamp_html.write(timestamp)
    timestamp_html.close()
  # if

# if