#!/usr/bin/python
# -*- coding: utf-8 -*-

from os      import listdir
from netcdfio_irradiancia import netcdf2png, ncdump

cmapPath = './cmaps/'

# banda = ['banda01','banda02','banda03','banda04','banda06']

banda = ['banda03']

for b in banda:

  print b

  if b == 'banda01':
    ncpath = './B01/'
    cmap   = 'jet'
  elif b == 'banda02':
    ncpath = './B02/'
    cmap   = 'inumet'
  elif b == 'banda03':
    ncpath = './B03/'
    cmap   = 'inumet'
  elif b == 'banda04':
    ncpath = './B04/'
    cmap   = 'inumet'
  elif b == 'banda06':
    ncpath = './B06/'
    cmap   = 'gray'

  dirDest  = ncpath[:-1] + '_png/'

  lista = sorted(listdir(ncpath))

  # lista = ['goes12.2005.236.234514.BAND_02.nc']
  # goes12.2005.236.234514.BAND_02.nc.png
  # goes12.2005.236.234514.BAND_04.nc.png

  for rootname in lista:
    file = ncpath + rootname
    ncdump(file)
    netcdf2png(file, cmapPath, cmap, dirDest, 'lat', 'lon', 'data')
    # netcdf2png(file, cmapPath, 'jet', dirDest, 'y', 'x','CMI', geos=True)
