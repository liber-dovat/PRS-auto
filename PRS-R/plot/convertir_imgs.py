#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os

from file_to_png import fileToPng

archivo1 = 'ART_2018302_180037'
archivo2 = 'ART_2018312_143036'

folder001 = 'ART_G001x001GG_C001x001'
folder005 = 'ART_G005x005GG_C005x005'
folder010 = 'ART_G010x010GG_C010x010'
folder015 = 'ART_G015x015GG_C015x015'

cmapPath = '/home/ldovat/dev/PRS-sat/PRS-R/plot/cmaps/'
PATHpng  = '/home/ldovat/dev/PRS-sat/PRS-R/plot/png/'
FileFR   = '/home/ldovat/dev/PRS-sat/PRS-R/data/prd/' + folder010 + '/B01-FR/2018/' + archivo2 + '.FR'
FileRP   = '/home/ldovat/dev/PRS-sat/PRS-R/data/prd/' + folder010 + '/B01-RP/2018/' + archivo2 + '.RP'
meta     = '/home/ldovat/dev/PRS-sat/PRS-R/data/prd/' + folder010 + '/meta/'

# si no existen los pngs los creo
# fileToPng(FileFR, meta15, cmapPath, 'jet', PATHpng)
fileToPng(FileRP, meta, cmapPath, 'inumet', PATHpng)
