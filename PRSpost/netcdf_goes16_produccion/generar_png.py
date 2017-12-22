#!/usr/bin/python
# -*- coding: utf-8 -*-

from netcdfio_irradiancia import netcdf2png, ncdump

goespath = './nc/'
dirDest  = './'
cmapPath = './cmaps/'

cmi_list = ['OR_ABI-L2-CMIPF-M3C01_G16_s20173521300426_e20173521311193_c20173521311264.nc',\
            'OR_ABI-L2-CMIPF-M3C02_G16_s20173481615413_e20173481626180_c20173481630509.nc']

rad_list = ['OR_ABI-L1b-RadF-M3C03_G16_s20173521300426_e20173521311193_c20173521311239.nc',\
            'OR_ABI-L1b-RadF-M3C04_G16_s20173521300426_e20173521311193_c20173521311219.nc',\
            'OR_ABI-L1b-RadF-M3C05_G16_s20173521330426_e20173521341193_c20173521341236.nc',\
            'OR_ABI-L1b-RadF-M3C06_G16_s20173521300426_e20173521311198_c20173521311236.nc',\
            'OR_ABI-L1b-RadF-M3C07_G16_s20173521300426_e20173521311204_c20173521311239.nc',\
            'OR_ABI-L1b-RadF-M3C08_G16_s20173521300426_e20173521311193_c20173521311239.nc',\
            'OR_ABI-L1b-RadF-M3C09_G16_s20173521300426_e20173521311199_c20173521311264.nc',\
            'OR_ABI-L1b-RadF-M3C10_G16_s20173521300426_e20173521311205_c20173521311258.nc',\
            'OR_ABI-L1b-RadF-M3C11_G16_s20173521300426_e20173521311193_c20173521311256.nc',\
            'OR_ABI-L1b-RadF-M3C12_G16_s20173521300426_e20173521311198_c20173521311261.nc',\
            'OR_ABI-L1b-RadF-M3C13_G16_s20173521300426_e20173521311204_c20173521311264.nc',\
            'OR_ABI-L1b-RadF-M3C14_G16_s20173521300426_e20173521311193_c20173521311259.nc',\
            'OR_ABI-L1b-RadF-M3C15_G16_s20173521300426_e20173521311199_c20173521311262.nc',\
            'OR_ABI-L1b-RadF-M3C16_G16_s20173521300426_e20173521311204_c20173521311263.nc']

for i in cmi_list:
  file = goespath + str(i)
  ncdump(file)
  netcdf2png(file, cmapPath, 'jet', dirDest, 'y', 'x','CMI')
  netcdf2png(file, cmapPath, 'jet', dirDest, 'y', 'x','CMI', geos=True)

# for i in rad_list:
#   file = goespath + str(i)
#   ncdump(file)
#   netcdf2png(file, cmapPath, 'jet', dirDest, 'y', 'x','Rad')
#   netcdf2png(file, cmapPath, 'jet', dirDest, 'y', 'x','Rad', geos=True)
