#!/usr/bin/python
# -*- coding: utf-8 -*-

from netcdfio_irradiancia import netcdf2png, ncdump

path     = './'
goespath = './goes-r/'
nc       = 'S10635335_201710251430.nc'
dirDest  = './'
cmapPath = dirDest + '/cmaps/'


# ncdump(path + nc)
# netcdf2png(path + nc, cmapPath, 'jet', dirDest, 'lat', 'lon','Band1')

# MEM ERROR - Memoria insuficiente
# file02 = goespath + 'band02/' + 'OR_ABI-L2-CMIPF-M4C02_G16_s20171971905222_e20171971910023_c20171971910090-114300_0.nc'
# ncdump(file02)
# netcdf2png(file02, cmapPath, 'inumet', dirDest, 'y', 'x','CMI')
# netcdf2png(file02, cmapPath, 'inumet', dirDest, 'y', 'x','CMI', geos=True)

file07 = goespath + 'band07/' + 'OR_ABI-L2-CMIPF-M4C07_G16_s20171971910222_e20171971915036_c20171971915108.nc'
ncdump(file07)
netcdf2png(file07, cmapPath, 'inumet', dirDest, 'y', 'x','CMI')
netcdf2png(file07, cmapPath, 'inumet', dirDest, 'y', 'x','CMI', geos=True)

file08 = goespath + 'band08/' + 'OR_ABI-L2-CMIPF-M3C08_G16_s20171921715382_e20171921726149_c20171921726222.nc'
ncdump(file08)
netcdf2png(file08, cmapPath, 'inumet', dirDest, 'y', 'x','CMI')
netcdf2png(file08, cmapPath, 'inumet', dirDest, 'y', 'x','CMI', geos=True)

file09 = goespath + 'band09/' + 'OR_ABI-L2-CMIPF-M3C09_G16_s20171921715382_e20171921726155_c20171921726229.nc'
ncdump(file09)
netcdf2png(file09, cmapPath, 'inumet', dirDest, 'y', 'x','CMI')
netcdf2png(file09, cmapPath, 'inumet', dirDest, 'y', 'x','CMI', geos=True)

file13 = goespath + 'band13/' + 'OR_ABI-L2-CMIPF-M4C13_G16_s20171971905222_e20171971910035_c20171971910106.nc'
ncdump(file13)
netcdf2png(file13, cmapPath, 'inumet', dirDest, 'y', 'x','CMI')
netcdf2png(file13, cmapPath, 'inumet', dirDest, 'y', 'x','CMI', geos=True)

file14 = goespath + 'band14/' + 'OR_ABI-L2-CMIPF-M3C14_G16_s20171921700382_e20171921711149_c20171921711230.nc'
ncdump(file14)
netcdf2png(file14, cmapPath, 'inumet', dirDest, 'y', 'x','CMI')
netcdf2png(file14, cmapPath, 'inumet', dirDest, 'y', 'x','CMI', geos=True)

file15 = goespath + 'band15/' + 'OR_ABI-L2-CMIPF-M3C15_G16_s20172011615381_e20172011626153_c20172011626325.nc'
ncdump(file15)
netcdf2png(file15, cmapPath, 'inumet', dirDest, 'y', 'x','CMI')
netcdf2png(file15, cmapPath, 'inumet', dirDest, 'y', 'x','CMI', geos=True)