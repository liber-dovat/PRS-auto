#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import struct
import netCDF4
import numpy
import math
import os
import gc
import re

from mpl_toolkits.basemap import Basemap, shiftgrid
from os.path              import basename
from pyproj               import Proj
from utils                import gmtColormap, ncdump

#########################################
#########################################
#########################################

def channelInfo(channelNumber):
  if channelNumber == 'C01':
    print "ABI L2+ "
    print "Range: 0.0166056 to 0.9999 1"
    print "Wavelength: 0.45~0.49 um"
  elif channelNumber == 'C02':
    print "ABI L2+ "
    print "Range: 206.647 to 313.627 K"
    print "Wavelength: 0.60~0.68 um"
  elif channelNumber == 'C04':
    print "ABI L2+ "
    print "Range: 206.647 to 313.627 K"
    print "Wavelength: 1.36~1.38 um"
  elif channelNumber == 'C13':
    print "ABI L2+ "
    print "Range: 206.647 to 313.627 K"
    print "Wavelength: 10.2~10.5 um"

# end channelInfo

#########################################
#########################################
#########################################

def rangoColorbar(channel):

  # defino los rangos del colorbar en funcion del tipo de banda
  if channel == 'C01':
    vmin = 0
    vmax = 100
  elif channel == 'C02':
    vmin = 0
    vmax = 100
  elif channel == 'C04':
    vmin = 0
    vmax = 100
  elif channel == 'C07':
    vmin = -80.3
    vmax = 70
  elif channel == 'C08':
    vmin = -60
    vmax = 0
  elif channel == 'C09':
    vmin = -60
    vmax = 0
  elif channel == 'C13':
    vmin = -80.3
    vmax = 70
  elif channel == 'C14':
    vmin = -80.3
    vmax = 70
  elif channel == 'C15':
    vmin = -80.3
    vmax = 70

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

  t_coverage = repr(nc_fid.getncattr('time_coverage_end'))
  # print t_coverage

  ds_name = repr(nc_fid.getncattr('dataset_name'))
  # print ds_name

  date = re.search('\'(.*?)\'', t_coverage).group(1)
  print date

  channel = re.search('-M\d(.*?)_', ds_name).group(1)
  print channel

  channelInfo(channel)

  yl = date[0:4]
  yy = date[2:4]
  mt = date[5:7]
  dd = date[8:10]
  hh = date[11:13]
  mm = date[14:16]
  ss = date[17:19]

  name     = channel + " " + dd + "-" + mt + "-" + yl + " " + hh + ":" + mm + " UTC"
  filename = channel + "_" + yy + mt + dd + "_" + hh + mm + ss
  # print "name: " + name

  # extract/copy the data
  data = nc_fid.variables[data_name][:]

  # print "Data min: " + str(numpy.amin(data))
  # print "Data max: " + str(numpy.amax(data))

  if channel == 'C01' or channel == 'C02':
    data /= numpy.amax(data)
    data *= 100
  elif channel == 'C04':
    data /= numpy.amax(data)
    data *= 200
  elif channel == 'C13':
    # Los datos estan en kelvin, asi que los paso a Celsius
    data -= 273.15

  # print str(data)

  # print "Data min: " + str(numpy.amin(data))
  # print "Data max: " + str(numpy.amax(data))

  if data_name == 'CMI' or data_name == 'Rad':
    # Satellite height
    sat_h = nc_fid.variables['goes_imager_projection'].perspective_point_height
    sat_h += 25000
    # Satellite longitude
    sat_lon = nc_fid.variables['goes_imager_projection'].longitude_of_projection_origin
    # Satellite sweep
    sat_sweep = nc_fid.variables['goes_imager_projection'].sweep_angle_axis
    X = nc_fid.variables[lon_name][:] * sat_h # longitud, eje X
    Y = nc_fid.variables[lat_name][:] * sat_h # latitud, eje Y

    # print "sat_h: "   + str(sat_h)
    # print "Sat_lon: " + str(sat_lon);

    # print "len X:" + str(len(X))
    # print "len Y:" + str(len(Y))

    scene_id_val = repr(nc_fid.getncattr('scene_id'))
    scene_id     = re.search('\'(.*?)\'', scene_id_val).group(1)

    if scene_id == 'Full Disk':
      print "Generando el recorte según porcentajes para Full Disk"

      factor_x_min = 55.2 # %
      factor_x_max = 76.6
      factor_y_min = 71.2
      factor_y_max = 88.5

      xmin = numpy.int_(numpy.floor(factor_x_min * len(X) / 100))
      xmax = numpy.int_(numpy.floor(factor_x_max * len(X) / 100))
      ymin = numpy.int_(numpy.floor(factor_y_min * len(Y) / 100))
      ymax = numpy.int_(numpy.floor(factor_y_max * len(Y) / 100))

      # print "xmin: " + str(xmin) 
      # print "xmax: " + str(xmax) 
      # print "ymin: " + str(ymin) 
      # print "ymax: " + str(ymax)

      # parche para hacer coincidir las imágenes
      ymin = xmin
      xmax = ymax

      # si el canal es el 2 divido las dimensiones de los elementos
      if not geos:
        X = X[xmin:xmax]
        Y = Y[ymin:ymax]
        data = data[xmin:xmax, ymin:ymax]

      # if not geos and  channel == 'C01':
      #   X = X[6000:10000]
      #   Y = Y[6000:10000]
      #   data = data[6000:10000, 6000:10000]
      # elif not geos and channel == 'C02':
      #   X = X[11997:16982]
      #   Y = Y[11997:16982]
      #   data = data[11997:16982, 11997:16982]
      # elif not geos:
      #   X = X[2000:4800]
      #   Y = Y[2000:4800]
      #   data = data[2000:4800, 2000:4800]
      elif geos:
        X = X[::4]
        Y = Y[::4]
        data = data[::4, ::4]

    # end if fulldisk

  nc_fid.close()

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  # axes = plt.gca()
  # axes.set_xlim([min_lon, max_lon])
  # axes.set_ylim([min_lat, max_lat])

  zona = 'plata'

  if zona == 'plata' and not geos: # proyecto con mercator en la región del río de la plata
    print "Ventana Río de la Plata"

    # https://github.com/blaylockbk/pyBKB_v2/blob/master/BB_goes16/mapping_GOES16_data.ipynb

    min_Y = numpy.amin(Y)
    max_Y = numpy.amax(Y)
    min_X = numpy.amin(X)
    max_X = numpy.amax(X)

    # parche para alinear la fotografía con las coordenadas geográficas
    # supongo que una vez esté calibrado el satélite hay que eliminar estas líneas
    X = map(lambda x: x+5000, X) # incremento X
    Y = map(lambda y: y+5000, Y) # incremento Y

    # print "min_Y: " + str(min_Y)
    # print "max_Y: " + str(max_Y)
    # print "min_X: " + str(min_X)
    # print "max_X: " + str(max_X)

    # print numpy.amin(X)
    # print numpy.amin(Y)

    # Región
    ax = Basemap(projection='merc',\
            llcrnrlat=-42.94,urcrnrlat=-22.0,\
            llcrnrlon=-67.0,urcrnrlon=-45.04,\
            resolution='f')

    projection     = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)
    x_mesh, y_mesh = numpy.meshgrid(X,Y)
    lons, lats     = projection(x_mesh, y_mesh, inverse=True)
    x, y           = ax(lons, lats)

  elif geos: # proyecto toda la foto completa de geo estacionario
    print "Ventana Globo geoestacionario"

    min_Y = numpy.amin(Y)
    max_Y = numpy.amax(Y)
    min_X = numpy.amin(X)
    max_X = numpy.amax(X)

    XX = map(lambda x: x+max_X, X) # incremento X
    YY = map(lambda y: y+max_Y, Y) # incremento Y

    x, y = numpy.meshgrid(XX,YY)

    ax = Basemap(projection='geos', lon_0=sat_lon, satellite_height=sat_h,\
                  llcrnrx=-5429619.5,llcrnry=-5433126.0,\
                  urcrnrx=5429619.5,urcrnry=5433126.0,\
                  resolution='l')

  # end if

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  # agrego los vectores de las costas, departamentos/estados/provincias y paises
  ax.drawcoastlines(linewidth=0.50)
  ax.drawcountries(linewidth=0.50)
  ax.drawstates(linewidth=0.25)

  if not geos:
    # dibujo los valores de latitudes y longitudes al margen de la imagen
    par = ax.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10, color='white')
    mer = ax.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10, color='white')
    setcolor(par,'white')
    setcolor(mer,'white')

  # defino el min y max en funcion de la banda
  vmin, vmax = rangoColorbar(channel)

  data = numpy.ma.masked_where(numpy.isnan(data), data)

  # dibujo img en las coordenadas x e y calculadas

  # cmap = gmtColormap(colormapName, colormapPath, 2048)

  # defino el colormap  y la disposicion de los ticks segun la banda
  if channel == 'C02' or channel == 'C01':
    ticks       = [0, 20, 40, 60, 80, 100]
    ticksLabels = ticks
  elif channel == 'C04':
    ticks       = [0, 20, 40, 60, 80, 100]
    ticksLabels = ticks
  else:
    ticks = [-80, -75.2, -70.2, -65.2, -60.2, -55.2, -50.2, -45.2, -40.2, -35.2, -30.2,-20,-10,0,10,20,30,40,50,60,70]
    # defino las etiquetas del colorbar
    ticksLabels = [-80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30,-20,-10,0,10,20,30,40,50,60,70]
  # if FR o RP

  cmap = gmtColormap(colormapName, colormapPath, 2048)
  cs   = ax.pcolormesh(x, y, data, vmin=vmin, vmax=vmax, cmap=cmap)

  # seteo los limites del colorbar
  plt.clim(vmin, vmax)

  # agrego el colorbar
  cbar = ax.colorbar(cs, location='bottom', pad='3%', ticks=ticks)

  if colormapName == 'inumet':
    cbar.ax.set_xticklabels(ticksLabels, rotation=45, fontsize=7, color='white')
  else:
    cbar.ax.set_xticklabels(ticksLabels, fontsize=7, color='white')

  cbar.ax.set_xlabel("Temperatura de brillo ($^\circ$C)", fontsize=7, color='white')

  if channel == 'C13':
    cbar.ax.xaxis.labelpad = 0

  # agrego el logo en el documento
  logo = plt.imread('/sat/PRS/dev/PRS-sat/PRSgoes/logo_300_bw.png')
  plt.figimage(logo, 5, 5)

  # si no existe la carpeta asociada a la banda la creo
  if not os.path.isdir(dirDest + channel):
    os.mkdir(dirDest + channel)
  # if

  # si no existe la carpeta asociada al ano la creo
  if not os.path.isdir(dirDest + channel + '/' + yl):
    os.mkdir(dirDest + channel + "/" + yl)
  # if

  outPath = dirDest + channel + "/" + yl + "/"

  # si estoy dibujando toda la proyección geos adjunto el string al nombre del archivo
  if geos:
    outPath = outPath + filename + '_geos.png' # determino el nombre del archivo a escribir
  else:
    outPath = outPath + filename + '.png' # determino el nombre del archivo a escribir

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  print outPath

  # genero el pie de la imagen, con el logo y la info del archivo
  plt.annotate(name, (0,0), (106, -60), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=14, family='monospace', color='white')

  # genero un dpi dinamico segun la imagen que quiero procesar
  # if channel == 'C04':
  #   dpi = 200
  # elif channel == 'C01' or channel == 'C02':
  #   dpi = 900
  #   # dpi = 300
  # else:
  #   dpi = 200

  plt.savefig(outPath, bbox_inches='tight', dpi=300, transparent=True) # , facecolor='#4F7293'

  # copio la ultima imagen de cada carpeta en la raiz PNG para subir a la web
  plt.savefig(dirDest + channel + '.png', bbox_inches='tight', dpi=300, transparent=True) # , facecolor='#4F7293'
  plt.close()

  if channel == 'C01':
    return yl+mt+dd+hh+mm+ss

# def netcdf2png
