#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from file_to_png import fileToPng
from shutil      import copyfile
from funciones   import ymd, getLastFile, copiar_frames

PATHpng = '/sat/prd-sat/PNGs/'

baseVIS = '/sat/prd-sat/ART_G015x015GG_C015x015/'

meta15  = baseVIS + 'meta/'

# lista = open(sys.argv[1], 'r')

lista = open('/sat/PRS/libs/PRS-auto/data/job_imglist_VIS1', 'r')

for f in lista:

  year, rootname = getYearRoot(f)

  print year
  print rootname

  FRpath  = baseVIS + 'B01-FR/' + year + '/' + rootname + '.FR'
  RPpath  = baseVIS + 'B01-RP/' + year + '/' + rootname + '.RP'

  fileToPng(FRpath,  meta15, PATHpng)
  fileToPng(RPpath,  meta15, PATHpng)

  # si es el ultimo archivo procesado
  if f == lista[-1]:

    # genero una copia de cada imagen para subir a la web
    file = PATHpng + 'B01-FR/' + year + '/' + rootname + '.png'
    copyfile(file, PATHpng + "BAND_01-FR.png")

    file = PATHpng + 'B01-RP/' + year + '/' + rootname + '.png'
    copyfile(file, PATHpng + "BAND_01-RP.png")

    copiar_frames(PATHpng + 'B01-FR/' + year, PATHpng + 'B01-FR/mp4')
    copiar_frames(PATHpng + 'B01-RP/' + year, PATHpng + 'B01-RP/mp4')

    doy       = rootname[8:11]                  # obtengo el doy del rootname
    hms       = rootname[12:18]                 # obtengo la hora minuto y segundo del rootname
    month     = ymd(int(year), int(doy))[1]     # obtengo el mes usando la funcion ymd
    timestamp = year + '.' + str(month).zfill(2) + '.' + str(doy).zfill(3) + '.' + hms

    timestamp_file = open(PATHpng + 'timestamp.html', 'w')
    timestamp_html.write(timestamp)
    timestamp_html.close()
  # if

# if