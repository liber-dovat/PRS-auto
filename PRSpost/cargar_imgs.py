#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import struct
import numpy
import os

from funciones    import ymd
from os.path      import basename
from inumet_color import _get_inumet
from mpl_toolkits.basemap import Basemap

# RUTAsat = '/sat/prd-sat/ART_G015x015GG_C015x015/'
# PATHfr  = RUTAsat + 'B01-FR/2016/ART_2016275_143500.FR'

# print PATHfr

def rangoColorbar(ext):

  # defino los rangos del colorbar en funcion del tipo de banda
  if ext == 'FR' or ext == 'RP':
    vmin = 0.
    vmax = 100.
  elif ext == 'T2':
    vmin = -68.
    vmax = 47. 
  elif ext == 'T3':
    vmin = -68.
    vmax = -8.
  elif ext == 'T4':
    vmin = -80.
    vmax = 50.
  elif ext == 'T6':
    vmin = -68.
    vmax = 7.

  return vmin, vmax

# rangoColorbar

#########################################
#########################################
#########################################

def bandTag(banda):

  if banda == 'FR':
    return "CH1 FR"
  elif banda == 'RP':
    return "CH1 RP"
  elif banda == 'T2':
    return "CH2 T2"
  elif banda == 'T3':
    return "CH3 T3"
  elif banda == 'T4':
    return "CH4 T4"
  elif banda == 'T6':
    return "CH6 T6"

# bandTag

#########################################
#########################################
#########################################

def getExt(url):
  name = basename(url)
  return name.split('.')[-1]
# getExt

#########################################
#########################################
#########################################

def nameTag(basename):
  name       = basename[:-3]
  name_split = name.split("_")
  year       = name_split[1][0:4]
  doy        = name_split[1][4:8]
  hms        = name_split[2]
  month      = ymd(int(year), int(doy))[1]
  day        = ymd(int(year), int(doy))[2]

  str_day   = str(day).zfill(2)
  str_month = str(month).zfill(2)
  str_hm    = hms[0:2] + ":" +hms[2:4]
  str_chnl  = bandTag(getExt(basename))

  return str_chnl + " " + str_day + "-" + str_month + "-" + year + " " + str_hm + " UTC"  
# nameTag

#########################################
#########################################
#########################################

def frtopng(metaPath, file):

  fid = open(metaPath + '/T000gri.META', 'r')
  meta = numpy.fromfile(fid, dtype='float32')
  fid.close()

  fid = open(metaPath + '/T000gri.LATvec', 'r')
  LATdeg_vec = numpy.fromfile(fid, dtype='float32')
  LATdeg_vec = LATdeg_vec[::-1] # invierto el arreglo porque quedaba invertido verticalmente
  fid.close()

  fid = open(metaPath + '/T000gri.LONvec', 'r')
  LONdeg_vec = numpy.fromfile(fid, dtype='float32')
  fid.close()

  # obtengo del vector meta el largo y alto de elementos de los vectores y los datos
  Ci = meta[0];
  Cj = meta[1];
  Ct = Ci*Cj;

  numpy.set_printoptions(suppress=True)

  print file
  # print meta
  # print Ci
  # print Cj
  # print Ct
  # print LATdeg_vec.size
  # print LATdeg_vec.size

  print "Lon min:" + str(numpy.amin(LONdeg_vec)) + ", Lon max:" + str(numpy.amax(LONdeg_vec))
  print "Lat min:" + str(numpy.amin(LATdeg_vec)) + ", Lat max:" + str(numpy.amax(LATdeg_vec))

  # plt.axis('scaled')

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  axes = plt.gca()
  axes.set_xlim([numpy.amin(LONdeg_vec),numpy.amax(LONdeg_vec)])
  axes.set_ylim([numpy.amin(LATdeg_vec),numpy.amax(LATdeg_vec)])

  # abro el archivo FR
  fid = open(file, 'r')
  data = numpy.fromfile(fid, dtype='float32')
  fid.close()
  # print data.shape
  IMG = numpy.reshape(data, (Ci, Cj))
  # print IMG.shape

  ax1 = Basemap(projection='merc',\
                llcrnrlat=numpy.amin(LATdeg_vec),urcrnrlat=numpy.amax(LATdeg_vec),\
                llcrnrlon=numpy.amin(LONdeg_vec),urcrnrlon=numpy.amax(LONdeg_vec),\
                resolution='l')

  ax1.drawcoastlines()
  ax1.drawstates()
  ax1.drawcountries()

  # dibujo los valores de latitudes y longitudes
  ax1.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10)
  ax1.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10)

  lons2d, lats2d = numpy.meshgrid(LONdeg_vec, LATdeg_vec)
  x, y = ax1(lons2d,lats2d)

  ext = getExt(file)

  vmin, vmax = rangoColorbar(ext)

  # grafico IMG1 usando lon como vector x y lat como vector y
  # dado que FR y RP van de 0 a 100 seteo esos rangos para el colorbar
  if ext == 'FR' or ext == 'RP':
    cs = ax1.pcolormesh(x, y, IMG, vmin=vmin, vmax=vmax, cmap='jet')
    plt.clim(vmin, vmax)

    ticks=[0., 20., 40., 60., 80., 100.]
  else:

    # Los datos de T2 a T6 estan en kelvin, asi que los paso a Celsius
    IMG -= 273.

    inumet = _get_inumet(1024)
    cs = ax1.pcolormesh(x, y, IMG, vmin=vmin, vmax=vmax, cmap=inumet)

    ticks=[vmin, 0., vmax]

  # if FR o RP

  # agrego el colorbar
  cbar = ax1.colorbar(cs, location='bottom', pad='3%', ticks=ticks)
  cbar.ax.set_xticklabels(ticks, fontsize=10)

  # agrego el logo en el documento
  logo = plt.imread('/sat/PRS/libs/PRS-auto/PRSpng/imgs/les-logo.png')
  plt.figimage(logo, 5, 5)

  # genero los datos para escribir el pie de pagina
  name     = basename(file)           # obtengo el nombre base del archivo
  PATHpng = './test/png/'
  destFile = PATHpng + ext + name +'.png' # determino el nombre del archivo a escribir

  tag = nameTag(name)

  # genero el pie de la imagen, con el logo y la info del arcivo
  plt.annotate(tag, (0,0), (140, -50), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=10, family='monospace')

  plt.savefig(destFile, bbox_inches='tight', dpi=200)
  plt.close() # cierro el archivo

# frtopng

frtopng('./test/meta15/', './test/imgs/ART_2016285_133500.FR')
frtopng('./test/meta15/', './test/imgs/ART_2016285_133500.RP')
frtopng('./test/meta60/', './test/imgs/ART_2016285_133500.T2')
frtopng('./test/meta60/', './test/imgs/ART_2016285_133500.T3')
frtopng('./test/meta60/', './test/imgs/ART_2016285_133500.T4')
frtopng('./test/meta60/', './test/imgs/ART_2016285_133500.T6')
