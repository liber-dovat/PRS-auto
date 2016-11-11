#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os

from os.path     import isfile
from file_to_png import fileToPng
from shutil      import copyfile
from funciones   import ymd, getLastFile, copiar_frames, getRootnameYear, getDateArray, lastReceived

prs_path  = '/sat/PRS/libs/PRS-auto/data/last-image-prs'
rcv_path  = '/sat/PRS/libs/PRS-auto/data/last-image-rcv'
file_path = '/sat/prd-sat/ART_G015x015GG_C015x015/B01-FR/'

PATHpng = '/sat/prd-sat/PNGs/'
baseVIS = '/sat/prd-sat/ART_G015x015GG_C015x015/'
baseIR  = '/sat/prd-sat/ART_G060x060GG_C060x060/'

lastReceived(file_path, rcv_path)

lista = getDateArray(prs_path, rcv_path, file_path)

for rootname in lista:

  year = getRootnameYear(rootname)

  print rootname

  meta15  = baseVIS + 'meta/'
  meta60  = baseIR  + 'meta/'

  FRpath  = baseVIS + 'B01-FR/' + year + '/' + rootname + '.FR'
  RPpath  = baseVIS + 'B01-RP/' + year + '/' + rootname + '.RP'
  B02path = baseIR  + 'B02-T2/' + year + '/' + rootname + '.T2'
  B03path = baseIR  + 'B03-T3/' + year + '/' + rootname + '.T3'
  B04path = baseIR  + 'B04-T4/' + year + '/' + rootname + '.T4'
  B06path = baseIR  + 'B06-T6/' + year + '/' + rootname + '.T6'

  # si no existen los pngs los creo
  if not os.path.isfile(PATHpng + 'B01-FR/' + year + '/' + rootname + '.png') and os.path.isfile(FRpath):
    fileToPng(FRpath,  meta15, PATHpng)

  if not os.path.isfile(PATHpng + 'B01-RP/' + year + '/' + rootname + '.png') and os.path.isfile(RPpath):
    fileToPng(RPpath,  meta15, PATHpng)

  if not os.path.isfile(PATHpng + 'B02/' + year + '/' + rootname + '.png') and os.path.isfile(B02path):
    fileToPng(B02path, meta60, PATHpng)

  if not os.path.isfile(PATHpng + 'B03/' + year + '/' + rootname + '.png') and os.path.isfile(B03path):
    fileToPng(B03path, meta60, PATHpng)

  if not os.path.isfile(PATHpng + 'B04/' + year + '/' + rootname + '.png') and os.path.isfile(B04path):
    fileToPng(B04path, meta60, PATHpng)

  if not os.path.isfile(PATHpng + 'B06/' + year + '/' + rootname + '.png') and os.path.isfile(B06path):
    fileToPng(B06path, meta60, PATHpng)

  # escribo la ultima procesada
  ultima_procesada = open(prs_path, 'w')
  ultima_procesada.write(rootname)
  ultima_procesada.close()

  # si procese el ultimo elemento de la lista
  if rootname == lista[-1]:

    # genero una copia de cada imagen para subir a la web
    fileFR = PATHpng + 'B01-FR/' + year + '/' + rootname + '.png'
    fileRP = PATHpng + 'B01-RP/' + year + '/' + rootname + '.png'
    file02 = PATHpng + 'B02/'    + year + '/' + rootname + '.png'
    file03 = PATHpng + 'B03/'    + year + '/' + rootname + '.png'
    file04 = PATHpng + 'B04/'    + year + '/' + rootname + '.png'
    file06 = PATHpng + 'B06/'    + year + '/' + rootname + '.png'

    copyfile(fileFR, PATHpng + "BAND_01-FR.png")
    copyfile(fileRP, PATHpng + "BAND_01-RP.png")
    copyfile(file02, PATHpng + "BAND_02.png")
    copyfile(file03, PATHpng + "BAND_03.png")
    copyfile(file04, PATHpng + "BAND_04.png")
    copyfile(file06, PATHpng + "BAND_06.png")

    subprocess.call("/sat/PRS/libs/PRS-auto/PRSpost/rmframes.sh", shell=True)

    # copio los frames
    copiar_frames(PATHpng + 'B04/'    + year, PATHpng + 'B04/mp4')
    copiar_frames(PATHpng + 'B01-FR/' + year, PATHpng + 'B01-FR/mp4')
    copiar_frames(PATHpng + 'B01-RP/' + year, PATHpng + 'B01-RP/mp4')

    # genero el timestamp
    doy   = rootname[8:11]                  # obtengo el doy del rootname
    hms   = rootname[12:18]                 # obtengo la hora minuto y segundo del rootname
    month = ymd(int(year), int(doy))[1]     # obtengo el mes usando la funcion ymd
    timestamp  = year + '.' + str(month).zfill(2) + '.' + str(doy).zfill(3) + '.' + hms

    timestamp_html = open(PATHpng + 'timestamp.html', 'w')
    timestamp_html.write(timestamp)
    timestamp_html.close()

    subprocess.call("/sat/PRS/libs/PRS-auto/PRSpost/videoandcopy.sh", shell=True)
  # if

# if