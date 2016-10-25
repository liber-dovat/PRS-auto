#!/usr/bin/python
# -*- coding: utf-8 -*-

from file_to_png import fileToPng
from get_file    import getLastFile

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
