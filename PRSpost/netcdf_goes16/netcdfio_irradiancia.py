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

def rangoColorbar(channel):

  # defino los rangos del colorbar en funcion del tipo de banda
  if channel == 'C02':
    vmin = 0
    vmax = 100
  elif channel == 'C07':
    vmin = -70
    vmax = 70
  elif channel == 'C08':
    vmin = -100
    vmax = 30
  elif channel == 'C09':
    vmin = -100
    vmax = 30
  elif channel == 'C13':
    vmin = -80
    vmax = 70
  elif channel == 'C14':
    vmin = -100
    vmax = 70
  elif channel == 'C15':
    vmin = -100
    vmax = 70

  return vmin, vmax

# rangoColorbar

#########################################
#########################################
#########################################

def netcdf2png(url, colormapPath, colormapName, dirDest, lat_name, lon_name, data_name, geos=False):
  
  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')

  if data_name == 'Band1':
    name = basename(url)           # obtengo el nombre base del archivo
  else:
    t_coverage = repr(nc_fid.getncattr('time_coverage_end'))
    # print t_coverage

    ds_name = repr(nc_fid.getncattr('dataset_name'))
    # print ds_name

    date = re.search('\'(.*?)\'', t_coverage).group(1)
    print date

    channel = re.search('-M\d(.*?)_', ds_name).group(1)
    print channel

    channelInfo(channel)

    name = channel + "_" + date
  # if name

  # extract/copy the data
  lats = nc_fid.variables[lat_name][:]
  lons = nc_fid.variables[lon_name][:]
  data = nc_fid.variables[data_name][:]

  if data_name == 'CMI':
    # Satellite height
    sat_h = nc_fid.variables['goes_imager_projection'].perspective_point_height
    sat_h -= 10000
    # Satellite longitude
    sat_lon = nc_fid.variables['goes_imager_projection'].longitude_of_projection_origin
    # Satellite sweep
    sat_sweep = nc_fid.variables['goes_imager_projection'].sweep_angle_axis
    X = nc_fid.variables[lon_name][:] * sat_h # longitud, eje X
    Y = nc_fid.variables[lat_name][:] * sat_h # latitud, eje Y

    # si el canal es el 2 divido las dimensiones de los elementos
    # if channel == 'C15':
    #   X = X[::4]
    #   Y = Y[::4]
    #   data = data[::4, ::4]

    # if not geos:
    #   X = X[::4]
    #   Y = Y[::4]
    #   data = data[::4, ::4]

    print "sat_h: " + str(sat_h)

    # if nc_fid.variables[data_name].units == "K":
      # data = map(lambda d: d-273, data) # paso data a grados C

    print "Sat_lon: "   + str(sat_lon);

  # end if data_name == 'CMI'

  nc_fid.close()

  min_lon = numpy.amin(lons)
  max_lon = numpy.amax(lons)
  min_lat = numpy.amin(lats)
  max_lat = numpy.amax(lats)

  print "min_lat: " + str(min_lon)
  print "max_lat: " + str(max_lon)
  print "min_lon: " + str(min_lat)
  print "max_lon: " + str(max_lat)

  # for i in data:
  #   print i

  print "Data min: " + str(numpy.amin(data))
  print "Data max: " + str(numpy.amax(data))

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  # axes = plt.gca()
  # axes.set_xlim([min_lon, max_lon])
  # axes.set_ylim([min_lat, max_lat])

  zona = 'plata'

  if data_name == 'Band1': # para archivos nc ya proyectados a mercator

    X = map(lambda x: x+0.11, lons) # incremento X
    Y = map(lambda y: y+0.11, lats) # incremento Y

    ax1 = Basemap(projection='merc',\
                  llcrnrlat=-42.94,urcrnrlat=-22.0,\
                  llcrnrlon=-67.0,urcrnrlon=-45.04,\
                  resolution='f')
    # resolution: c, l, i, h, f

    lons2d, lats2d = numpy.meshgrid(X, Y)
    # dadas las lat y lon del archivo, obtengo las coordenadas x y para
    # la ventana seleccionada como proyeccion
    x, y = ax1(lons2d,lats2d)

  elif geos: # proyecto toda la foto completa de geo estacionario
    print "Ventana Globo geoestacionario"

    min_Y = numpy.amin(Y)
    max_Y = numpy.amax(Y)
    min_X = numpy.amin(X)
    max_X = numpy.amax(X)

    XX = map(lambda x: x+max_X, X) # incremento X
    YY = map(lambda y: y+max_Y, Y) # incremento Y

    print "min_Y: " + str(min_Y)
    print "max_Y: " + str(max_Y)
    print "min_X: " + str(min_X)
    print "max_X: " + str(max_X)

    print numpy.amin(XX)
    print numpy.amin(YY)

    x, y = numpy.meshgrid(XX,YY)

    ax1 = Basemap(projection='geos', lon_0=sat_lon, satellite_height=sat_h,\
                  llcrnrx=-x.max()/2,llcrnry=-y.max()/2,\
                  urcrnrx=x.max()/2,urcrnry=y.max()/2,\
                  resolution='l')

  elif zona == 'plata': # proyecto con mercator en la región del río de la plata
    print "Ventana Ŕío de la Plata"

    # https://github.com/blaylockbk/pyBKB_v2/blob/master/BB_goes16/mapping_GOES16_data.ipynb

    min_Y = numpy.amin(Y)
    max_Y = numpy.amax(Y)
    min_X = numpy.amin(X)
    max_X = numpy.amax(X)

    # parche para alinear la fotografía con las coordenadas geográficas
    # supongo que una vez esté calibrado el satélite hay que eliminar estas líneas
    X = map(lambda x: x+10000, X) # incremento X
    Y = map(lambda y: y+10000, Y) # incremento Y

    print "min_Y: " + str(min_Y)
    print "max_Y: " + str(max_Y)
    print "min_X: " + str(min_X)
    print "max_X: " + str(max_X)

    print numpy.amin(X)
    print numpy.amin(Y)

    # Región
    ax1 = Basemap(projection='merc',\
            llcrnrlat=-42.94,urcrnrlat=-22.0,\
            llcrnrlon=-67.0,urcrnrlon=-45.04,\
            resolution='f')

    projection     = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)
    x_mesh, y_mesh = numpy.meshgrid(X,Y)
    lons, lats     = projection(x_mesh, y_mesh, inverse=True)
    x, y           = ax1(lons, lats)

  elif zona == 'sur': # proyecto con mercator en la región del río de la plata
    print "Ventana Sur"

    # https://github.com/blaylockbk/pyBKB_v2/blob/master/BB_goes16/mapping_GOES16_data.ipynb

    min_Y = numpy.amin(Y)
    max_Y = numpy.amax(Y)
    min_X = numpy.amin(X)
    max_X = numpy.amax(X)

    # parche para alinear la fotografía con las coordenadas geográficas
    # supongo que una vez esté calibrado el satélite hay que eliminar estas líneas
    X = map(lambda x: x+10000, X) # incremento X
    Y = map(lambda y: y+3000, Y) # incremento Y
    # X = map(lambda x: x+10000, X) # incremento X
    # Y = map(lambda y: y+10000, Y) # incremento Y

    print "min_Y: " + str(min_Y)
    print "max_Y: " + str(max_Y)
    print "min_X: " + str(min_X)
    print "max_X: " + str(max_X)

    print numpy.amin(X)
    print numpy.amin(Y)

    # Región
    ax1 = Basemap(projection='merc',\
            llcrnrlat=-49.4947,urcrnrlat=-13.6169,\
            llcrnrlon=-73.4699,urcrnrlon=-39.2205,\
            resolution='f')

    projection     = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)
    x_mesh, y_mesh = numpy.meshgrid(X,Y)
    lons, lats     = projection(x_mesh, y_mesh, inverse=True)
    x, y           = ax1(lons, lats)

  elif zona == 'uy': # proyecto con mercator en la región del río de la plata
    print "Ventana Uruguay"

    # https://github.com/blaylockbk/pyBKB_v2/blob/master/BB_goes16/mapping_GOES16_data.ipynb

    min_Y = numpy.amin(Y)
    max_Y = numpy.amax(Y)
    min_X = numpy.amin(X)
    max_X = numpy.amax(X)

    # parche para alinear la fotografía con las coordenadas geográficas
    # supongo que una vez esté calibrado el satélite hay que eliminar estas líneas
    X = map(lambda x: x+10000, X) # incremento X
    Y = map(lambda y: y+10000, Y) # incremento Y

    print "min_Y: " + str(min_Y)
    print "max_Y: " + str(max_Y)
    print "min_X: " + str(min_X)
    print "max_X: " + str(max_X)

    print numpy.amin(X)
    print numpy.amin(Y)

    # Región
    ax1 = Basemap(projection='merc',\
            llcrnrlat=-35.2138,urcrnrlat=-29.7466,\
            llcrnrlon=-58.9073,urcrnrlon=-52.7591,\
            # llcrnrx=-x.max()/2,llcrnry=-y.max()/2,\
            # urcrnrx=x.max()/2,urcrnry=y.max()/2,\
            resolution='f')

    projection     = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)
    x_mesh, y_mesh = numpy.meshgrid(X,Y)
    lons, lats     = projection(x_mesh, y_mesh, inverse=True)
    x, y           = ax1(lons, lats)

  # end if

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  # Los datos de estan en kelvin, asi que los paso a Celsius
  data -= 273.15

  # defino el min y max en funcion de la banda
  if data_name == 'Band1':
    vmin = numpy.amin(data)
    vmax = numpy.amax(data)
  else:
    vmin, vmax = rangoColorbar(channel)

  print numpy.amin(data)
  print numpy.amax(data)

  data = numpy.ma.masked_where(numpy.isnan(data), data)

  # dibujo img en las coordenadas x e y calculadas

  cmap = gmtColormap(colormapName, colormapPath, 2048)
  cs   = ax1.pcolormesh(x, y, data, vmin=vmin, vmax=vmax, cmap=cmap)

  # cs.set_array(None)

  # seteo los limites del colorbar
  # plt.clim(vmin, vmax)

  # agrego los vectores de las costas, departamentos/estados/provincias y paises
  ax1.drawcoastlines(linewidth=0.25)
  ax1.drawcountries(linewidth=0.50)
  ax1.drawstates(linewidth=0.25)

  # dibujo los valores de latitudes y longitudes
  # ax1.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10)
  # ax1.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10)

  # agrego el colorbar
  cbar = ax1.colorbar(cs, location='bottom', pad='3%', ticks=[vmin, vmax])
  cbar.ax.set_xticklabels([math.floor(vmin), math.floor(vmax)], fontsize=3)

  # si estoy dibujando toda la proyección geos adjunto el string al nombre del archivo
  if geos:
    name = name + "_geos"

  destFile = dirDest + name + '.png' # determino el nombre del archivo a escribir

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  print destFile

  plt.savefig(destFile, bbox_inches='tight', dpi=300, transparent=True)
  plt.close()

# def netcdf2png
