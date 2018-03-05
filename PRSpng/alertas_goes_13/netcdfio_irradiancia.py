#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import struct
import netCDF4
import numpy
import math
import calendar
import os
import gc
import re

from mpl_toolkits.basemap import Basemap, shiftgrid
from os.path              import basename
from pyproj               import Proj
from utils                import gmtColormap, ncdump
from calibracion          import calibrarData

#########################################
#########################################
#########################################

def ymd(Y,N):
  """ given year = Y and day of year = N, return year, month, day
      Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """    
  if calendar.isleap(Y):
      K = 1
  else:
      K = 2
  M = int((9 * (K + N)) / 275.0 + 0.98)
  if N < 32:
      M = 1
  D = N - int((275 * M) / 9.0) + K * int((M + 9) / 12.0) + 30
  return Y, M, D

#########################################
#########################################
#########################################

def channelInfo(channelNumber):
  if channelNumber == 'C02':
    print "ABI L2+ Cloud and moisture imagery reflectance factor"
    print "Range: 0.0166056 to 0.9999 1"
    print "Wavelength: 0.64 um"

  elif channelNumber == 'C07':
    print "ABI L2+ Cloud and moisture imagery brightness temperature"
    print "Range: 244.253 to 323.885 K"
    print "Wavelength: 3.89 um"

  elif channelNumber == 'C08':
    print "ABI L2+ Cloud and moisture imagery brightness temperature"
    print "Range: 205.704 to 248.755 K"
    print "Wavelength: 6.17 um"

  elif channelNumber == 'C09':
    print "ABI L2+ Cloud and moisture imagery brightness temperature"
    print "Range: 206.136 to 258.388 K"
    print "Wavelength: 6.93 um"

  elif channelNumber == 'C13':
    print "ABI L2+ Cloud and moisture imagery brightness temperature"
    print "Range: 206.647 to 313.627 K"
    print "Wavelength: 10.33 um"

  elif channelNumber == 'C14':
    print "ABI L2+ Cloud and moisture imagery brightness temperature"
    print "Range: 206.018 to 311.465 K"
    print "Wavelength: 11.19 um"

  elif channelNumber == 'C15':
    print "ABI L2+ Cloud and moisture imagery brightness temperature"
    print "Range: 204.171 to 307.612 K"
    print "Wavelength: 12.27 um"

# end channelInfo

#########################################
#########################################
#########################################

def rangoColorbar(banda):

  # defino los rangos del colorbar en funcion del tipo de banda
  if banda == 'BAND_01':
    vmin = 0
    vmax = 100
  elif banda == 'BAND_02':
    vmin = 0
    vmax = 100
  elif banda == 'BAND_03':
    vmin = 0
    vmax = 100
  elif banda == 'BAND_04':
    vmin = 0
    vmax = 100
  elif banda == 'BAND_06':
    vmin = 0
    vmax = 100

  # elif channel == 'C07':
  #   vmin = -80.3
  #   vmax = 70
  # elif channel == 'C08':
  #   vmin = -60
  #   vmax = 0
  # elif channel == 'C09':
  #   vmin = -60
  #   vmax = 0
  # elif channel == 'C13':
  #   vmin = -80.3
  #   vmax = 70
  # elif channel == 'C14':
  #   vmin = -80.3
  #   vmax = 70
  # elif channel == 'C15':
  #   vmin = -80.3
  #   vmax = 70

  return vmin, vmax

#########################################
#########################################
#########################################

def setcolor(x, color):
  for m in x:
    for t in x[m][1]:
      t.set_color(color)

#########################################
#########################################
#########################################

def netcdf2png(url, colormapPath, colormapName, dirDest, lat_name, lon_name, data_name, geos=False):
  
  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')

  # extract/copy the data
  data = nc_fid.variables[data_name][0]

  X_mat = nc_fid.variables[lon_name][:]
  Y_mat = nc_fid.variables[lat_name][:]

  X = X_mat[0]  # longitud, eje X
  Y = numpy.transpose(Y_mat)[0]

  nc_fid.close()

  # xc, size: 976, lon
  # yc, size: 453, lat

  # print X
  # print Y
  print data

  print len(X)
  print len(Y)

 # mpl_toolkits.basemap.interp(datain, xin, yin, xout, yout, checkbounds=False, masked=False, order=1)¶
 # http://earthpy.org/interpolation_between_grids_with_basemap.html

  # a lon sumarle 2
  # a lat restarle 1

  # X = X[::4]
  # Y = Y[::4]

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  # axes = plt.gca()
  # axes.set_xlim([min_lon, max_lon])
  # axes.set_ylim([min_lat, max_lat])

  name = basename(url)

  banda = name[23:30]
  yyyy  = name[7:11]
  doy   = name[12:15]
  hh    = name[16:18]
  mm    = name[18:20]
  ss    = name[20:22]
  yyyy, mt, dd = ymd(int(yyyy),int(doy))

  note_name = banda + " " + str(dd).zfill(2) + "-" + str(mt).zfill(2) + "-" + str(yyyy) + " " + hh + ":" + mm

  print name
  print note_name

  band_num = int(banda[-1])
  print band_num

  # if banda == 'BAND_04':
  #   data /= numpy.amax(data)
  #   data *= 100
  # elif banda == 'BAND_01':
  #   data /= numpy.amax(data)
  #   data *= 100

  # data /= numpy.amax(data)
  # data *= 100

  zona = 'plata'

  if zona == 'plata' and not geos: # proyecto con mercator en la región del río de la plata
    print "Ventana Río de la Plata"

    X_mat = map(lambda x: x+0.05, X_mat) # incremento X lon, positivos mueven ->
    Y_mat = map(lambda y: y+0.04, Y_mat) # restarle Y lat, positivos mueven ^

    shape = (len(Y), len(X))                    # guardo el shape original de data
    # data_vector = numpy.reshape(data,numpy.size(data)) # genero un vector de data usando su size (largo*ancho)
    data  = calibrarData(band_num, data) # invoco la funcion sobre el vector
    img   = numpy.reshape(data, shape)    # paso el vector a matriz usando shape como largo y ancho

    print img.shape

    # Región
    ax = Basemap(projection='merc',\
              llcrnrlat=-42.94,urcrnrlat=-22.0,\
              llcrnrlon=-67.0,urcrnrlon=-45.04,\
              resolution='f')

    # ax = Basemap(projection='merc',\
    #           llcrnrlat=-80,urcrnrlat=80,\
    #           llcrnrlon=-179,urcrnrlon=179,\
    #           resolution='f')

    print numpy.amin(img)
    print numpy.amax(img)

    X_mat = numpy.reshape(X_mat, shape)
    Y_mat = numpy.reshape(Y_mat, shape)

    # lons, lats = numpy.meshgrid(X_mat,Y_mat)
    x, y = ax(X_mat,Y_mat)

  # end if

  # agrego los vectores de las costas, departamentos/estados/provincias y paises
  ax.drawcoastlines(linewidth=0.25)
  ax.drawcountries(linewidth=0.50)
  ax.drawstates(linewidth=0.25)

  if not geos:
    # dibujo los valores de latitudes y longitudes al margen de la imagen
    par = ax.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10, color='white')
    mer = ax.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10, color='white')
    setcolor(par,'white')
    setcolor(mer,'white')

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  # vmin = 0
  # vmax = 100
  vmin, vmax = rangoColorbar(banda)

  img = numpy.ma.masked_where(numpy.isnan(img), img)

  # dibujo img en las coordenadas x e y calculadas

  # cmap = gmtColormap(colormapName, colormapPath, 2048)

  ticks       = [0, 20, 40, 60, 80, 100]
  ticksLabels = ticks

  # defino el colormap  y la disposicion de los ticks segun la banda
  if banda == 'BAND_01' or banda == 'BAND_02' or banda == 'BAND_03':
    ticks       = [0, 20, 40, 60, 80, 100]
    ticksLabels = ticks
  else:
    ticks = [-80, -75.2, -70.2, -65.2, -60.2, -55.2, -50.2, -45.2, -40.2, -35.2, -30.2,-20,-10,0,10,20,30,40,50,60,70]
    ticksLabels = [-80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30,-20,-10,0,10,20,30,40,50,60,70]
  # if FR o RP

  cmap = gmtColormap(colormapName, colormapPath, 2048)
  cs   = ax.pcolormesh(x, y, img, vmin=vmin, vmax=vmax, cmap=cmap)

  # seteo los limites del colorbar
  plt.clim(vmin, vmax)

  # agrego el colorbar
  cbar = ax.colorbar(cs, location='bottom', pad='3%', ticks=ticks)
  cbar.ax.set_xticklabels(ticksLabels, fontsize=7, color='white')

  if banda == 'BAND_01' or banda == 'BAND_02' or banda == 'BAND_03':
    cbar.ax.set_xticklabels(ticksLabels, fontsize=7, color='white')
  else:
    cbar.ax.set_xticklabels(ticksLabels, rotation=45, fontsize=7, color='white')

  cbar.ax.set_xlabel("Temperatura de brillo ($^\circ$C)", fontsize=7, color='white')

  # if banda != 'C02':
  #   cbar.ax.xaxis.labelpad = 0

  # agrego el logo en el documento
  logo = plt.imread('./logo_300_bw.png')
  plt.figimage(logo, 5, 5)

  # si estoy dibujando toda la proyección geos adjunto el string al nombre del archivo
  if geos:
    destFile = dirDest + name + '_geos.png' # determino el nombre del archivo a escribir
  else:
    destFile = dirDest + name + '.png' # determino el nombre del archivo a escribir

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  print destFile

# genero el pie de la imagen, con el logo y la info del archivo
  plt.annotate(note_name, (0,0), (106, -60), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=14, family='monospace', color='white')

  plt.savefig(destFile, bbox_inches='tight', dpi=200, transparent=True) # , facecolor='#4F7293'
  plt.close()

# def netcdf2png
