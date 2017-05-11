#!/usr/bin/python
# -*- coding: utf-8 -*-

from file_to_png_2 import fileToPng

Imgpath = '/home/ldovat/dev/PRS-auto/PRSpost/test/imgs/ART_2017131_174500.RP'
meta15  = '/home/ldovat/dev/PRS-auto/PRSpost/test/meta15'
PATHpng = '/home/ldovat/dev/PRS-auto/PRSpost/test/png/'

fileToPng(Imgpath,  meta15, PATHpng)
