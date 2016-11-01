#!/usr/bin/python
# -*- coding: utf-8 -*-

from file_to_png import fileToPng
from shutil      import copyfile
from funciones   import ymd, getLastFile, copiar_frames

year, rootname = getLastFile('/sat/prd-sat/ART_G015x015GG_C015x015/B01-FR/')

print year
print rootname

PATHpng = '/sat/prd-sat/PNGs/'

baseVIS = '/sat/prd-sat/ART_G015x015GG_C015x015/'
baseIR  = '/sat/prd-sat/ART_G060x060GG_C060x060/'

meta15  = baseVIS + 'meta/'
meta60  = baseIR  + 'meta/'

FRpath  = baseVIS + 'B01-FR/' + year + '/' + rootname + '.FR'
RPpath  = baseVIS + 'B01-RP/' + year + '/' + rootname + '.RP'
B02path = baseIR  + 'B02-T2/' + year + '/' + rootname + '.T2'
B03path = baseIR  + 'B03-T3/' + year + '/' + rootname + '.T3'
B04path = baseIR  + 'B04-T4/' + year + '/' + rootname + '.T4'
B06path = baseIR  + 'B06-T6/' + year + '/' + rootname + '.T6'

fileToPng(FRpath,  meta15, PATHpng)
fileToPng(RPpath,  meta15, PATHpng)
fileToPng(B02path, meta60, PATHpng)
fileToPng(B03path, meta60, PATHpng)
fileToPng(B04path, meta60, PATHpng)
fileToPng(B06path, meta60, PATHpng)

# genero una copia de cada imagen para subir a la web
file = PATHpng + 'B01-FR/' + year + '/' + rootname + '.png'
copyfile(file, PATHpng + "BAND_01-FR.png")

file = PATHpng + 'B01-RP/' + year + '/' + rootname + '.png'
copyfile(file, PATHpng + "BAND_01-RP.png")

file = PATHpng + 'B02/' + year + '/' + rootname + '.png'
copyfile(file, PATHpng + "BAND_02.png")

file = PATHpng + 'B03/' + year + '/' + rootname + '.png'
copyfile(file, PATHpng + "BAND_03.png")

file = PATHpng + 'B04/' + year + '/' + rootname + '.png'
copyfile(file, PATHpng + "BAND_04.png")

file = PATHpng + 'B06/' + year + '/' + rootname + '.png'
copyfile(file, PATHpng + "BAND_06.png")

# escribo el archivo timestamp con los datos de las imagenes
doy   = rootname[8:11]                  # obtengo el doy del rootname
hms   = rootname[12:18]                 # obtengo la hora minuto y segundo del rootname
month = ymd(int(year), int(doy))[1]     # obtengo el mes usando la funcion ymd
tsmp  = year + '.' + str(month).zfill(2) + '.' + str(doy).zfill(3) + '.' + hms
timestamp_html = open(PATHpng + 'timestamp.html', 'w')
timestamp_html.write(tsmp)
timestamp_html.close()

copiar_frames(PATHpng + 'B04/' + year, PATHpng + 'B04/mp4')
