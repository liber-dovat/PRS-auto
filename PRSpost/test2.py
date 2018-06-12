#!/usr/bin/python
# -*- coding: utf-8 -*-

from file_to_png import fileToPng
from shutil      import copyfile
from funciones   import ymd, getLastFile, lastReceived, getDateArray

PATHpng = '/sat/PRS/dev/PRS-sat/PRSpost/test/png/'

baseVIS = '/sat/PRS/dev/PRS-sat/PRSpost/test/imgs/'
baseIR  = '/sat/PRS/dev/PRS-sat/PRSpost/test/imgs/'

meta15  = '/sat/PRS/dev/PRS-sat/PRSpost/test/meta15'
meta60  = '/sat/PRS/dev/PRS-sat/PRSpost/test/meta60'

rootname = 'ART_2016285_133500'

FRpath  = baseVIS + rootname + '.FR'
RPpath  = baseVIS + rootname + '.RP'
B02path = baseIR  + rootname + '.T2'
B03path = baseIR  + rootname + '.T3'
B04path = baseIR  + rootname + '.T4'
B06path = baseIR  + rootname + '.T6'

# lastReceived()

#########################################
#########################################
# Defino las rutas a los archivos para poder trabajar con ellos
#########################################

# prs_path = '/sat/PRS/libs/PRS-sat/data/last-image-prs'
# rcv_path = '/sat/PRS/libs/PRS-sat/data/last-image-rcv'

prs_path  = '/sat/PRS/dev/PRS-sat/PRSpost/test/data/last-image-prs'
rcv_path  = '/sat/PRS/dev/PRS-sat/PRSpost/test/data/last-image-rcv'
file_path = '/sat/prd-sat/ART_G015x015GG_C015x015/B01-FR/'

# getDateArray(prs_path, rcv_path, file_path)

# fileToPng(FRpath,  meta15, PATHpng)
fileToPng(RPpath,  meta15, PATHpng)
# fileToPng(B02path, meta60, PATHpng)
# fileToPng(B03path, meta60, PATHpng)
# fileToPng(B04path, meta60, PATHpng)
# fileToPng(B06path, meta60, PATHpng)

# B2 = ['ART_2016304_230800',
# 'ART_2016304_233800',
# 'ART_2016304_234500',
# 'ART_2016305_003800',
# 'ART_2016305_010800',
# 'ART_2016305_013800',
# 'ART_2016305_020800',
# 'ART_2016305_023800',
# 'ART_2016305_024500',
# 'ART_2016305_033800',
# 'ART_2016305_040800',
# 'ART_2016305_043800',
# 'ART_2016305_050800',
# 'ART_2016305_053800',
# 'ART_2016305_054500',
# 'ART_2016305_063800',
# 'ART_2016305_070800',
# 'ART_2016305_073800',
# 'ART_2016305_080800',
# 'ART_2016305_083800',
# 'ART_2016305_084500',
# 'ART_2016305_093800',
# 'ART_2016305_100800',
# 'ART_2016305_103800',
# 'ART_2016305_110800',
# 'ART_2016305_113800',
# 'ART_2016305_123800',
# 'ART_2016305_130800',
# 'ART_2016305_133800',
# 'ART_2016305_140800',
# 'ART_2016305_143800',
# 'ART_2016305_144500',
# 'ART_2016305_160800',
# 'ART_2016305_163800',
# 'ART_2016305_170800',
# 'ART_2016305_173800',
# 'ART_2016305_174500',
# 'ART_2016305_183800',
# 'ART_2016305_190800',
# 'ART_2016305_193800',
# 'ART_2016305_200800',
# 'ART_2016305_203800',
# 'ART_2016305_204500',
# 'ART_2016305_213800',
# 'ART_2016305_220800',
# 'ART_2016305_223800',
# 'ART_2016305_230800',
# 'ART_2016305_233800',
# 'ART_2016305_234500',
# 'ART_2016306_003800',
# 'ART_2016306_010800',
# 'ART_2016306_013800',
# 'ART_2016306_020800',
# 'ART_2016306_023800',
# 'ART_2016306_024500',
# 'ART_2016306_033800',
# 'ART_2016306_040800',
# 'ART_2016306_043800',
# 'ART_2016306_050800',
# 'ART_2016306_053800',
# 'ART_2016306_054500',
# 'ART_2016306_063800',
# 'ART_2016306_070800',
# 'ART_2016306_073800',
# 'ART_2016306_080800',
# 'ART_2016306_083800',
# 'ART_2016306_084500',
# 'ART_2016306_093800',
# 'ART_2016306_100800',
# 'ART_2016306_103800',
# 'ART_2016306_110800',
# 'ART_2016306_113800',
# 'ART_2016306_114500',
# 'ART_2016306_123800',
# 'ART_2016306_130800',
# 'ART_2016306_133800',
# 'ART_2016306_140800',
# 'ART_2016306_143800',
# 'ART_2016306_144500',
# 'ART_2016306_160800',
# 'ART_2016306_163800',
# 'ART_2016306_170800',
# 'ART_2016306_174500',
# 'ART_2016306_183800',
# 'ART_2016306_190800',
# 'ART_2016306_193800',
# 'ART_2016306_200800']

# base = '/sat/PRS/dev/PRS-sat/PRSpost/test/alerta/'

# for rootname in B2:
#   print rootname
#   file = base + rootname + '.T4'
#   fileToPng(file, meta60, '/sat/PRS/dev/PRS-sat/PRSpost/test/alerta_png/')
