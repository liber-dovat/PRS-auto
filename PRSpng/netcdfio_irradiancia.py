#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import netCDF4
import struct
import numpy
import math
import os

from mpl_toolkits.basemap import Basemap
from os.path              import basename
# from funciones            import ymd
# from inumet_color         import _get_inumet
# from calibracion          import calibrarData

# http://scipy-cookbook.readthedocs.io/items/Matplotlib_Loading_a_colormap_dynamically.html
def gmtColormap(fileName,GMTPath = None,segmentos = 1024):
      import colorsys
      import numpy
      N = numpy
      if type(GMTPath) == type(None):
          filePath = "/usr/local/cmaps/"+ fileName+".cpt"
      else:
          filePath = GMTPath+"/"+ fileName +".cpt"
      try:
          f = open(filePath)
      except:
          print "file ",filePath, "not found"
          return None

      lines = f.readlines()
      f.close()

      x = []
      r = []
      g = []
      b = []
      colorModel = "RGB"
      for l in lines:
          ls = l.split()
          if l[0] == "#":
             if ls[-1] == "HSV":
                 colorModel = "HSV"
                 continue
             else:
                 continue
          if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
             pass
          else:
              x.append(float(ls[0]))
              r.append(float(ls[1]))
              g.append(float(ls[2]))
              b.append(float(ls[3]))
              xtemp = float(ls[4])
              rtemp = float(ls[5])
              gtemp = float(ls[6])
              btemp = float(ls[7])

      x.append(xtemp)
      r.append(rtemp)
      g.append(gtemp)
      b.append(btemp)

      nTable = len(r)
      x = N.array( x , N.float)
      r = N.array( r , N.float)
      g = N.array( g , N.float)
      b = N.array( b , N.float)
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "RGB":
          r = r/255.
          g = g/255.
          b = b/255.
      xNorm = (x - x[0])/(x[-1] - x[0])

      red = []
      blue = []
      green = []
      for i in range(len(x)):
          red.append([xNorm[i],r[i],r[i]])
          green.append([xNorm[i],g[i],g[i]])
          blue.append([xNorm[i],b[i],b[i]])
      colorDict = {"red":red, "green":green, "blue":blue}
      cwm = matplotlib.colors.LinearSegmentedColormap(fileName, colorDict, segmentos)
      return cwm

# gmtColormap

def ncdump(url, verb=True):
    '''
    http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print "\t\ttype:", repr(nc_fid.variables[key].dtype)
            for ncattr in nc_fid.variables[key].ncattrs():
                print '\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr))
        except KeyError:
            print "\t\tWARNING: %s does not contain variable attributes" % key
    # def print_ncattr

    # NetCDF global attributes
    nc_fid = netCDF4.Dataset(url, 'r')
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print "NetCDF Global Attributes:"
        for nc_attr in nc_attrs:
            print '\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions

    # Dimension shape information.
    if verb:
        print "NetCDF dimension information:"
        for dim in nc_dims:
            print "\tName:", dim 
            print "\t\tsize:", len(nc_fid.dimensions[dim])
            print_ncattr(dim)

    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print "NetCDF variable information:"
        for var in nc_vars:
            if var not in nc_dims:
                print '\tName:', var
                print "\t\tdimensions:", nc_fid.variables[var].dimensions
                print "\t\tsize:", nc_fid.variables[var].size
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

# def ncdump

#########################################
#########################################
#########################################

def bandTag(banda):

  if banda == 1:
    return "CH1 FR"
  elif banda == 2:
    return "CH2 T2"
  elif banda == 3:
    return "CH3 T3"
  elif banda == 4:
    return "CH4 T4"
  elif banda == 6:
    return "CH6 T6"

# nameTag

#########################################
#########################################
#########################################

def netcdf2png(url, dirDest):
  
  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')

  # extract/copy the data
  lats = nc_fid.variables['y'][:]
  lons = nc_fid.variables['x'][:]
  data = nc_fid.variables['z'][:]

  nc_fid.close()

  min_lon = numpy.amin(lons)
  max_lon = numpy.amax(lons)
  min_lat = numpy.amin(lats)
  max_lat = numpy.amax(lats)

  # for i in data:
  #   print i

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  axes = plt.gca()
  axes.set_xlim([min_lon, max_lon])
  axes.set_ylim([min_lat, max_lat])

  # ax1 = Basemap(projection='merc',\
  #             llcrnrlat=0.,urcrnrlat=68.516,\
  #             llcrnrlon=0.,urcrnrlon=179.341,\
  #             resolution='l')

  ax1 = Basemap(projection='merc',\
              llcrnrlat=min_lat,urcrnrlat=max_lat,\
              llcrnrlon=min_lon,urcrnrlon=max_lon,\
              resolution='l')

  # data  = data[0]                                    # me quedo con el primer elemento de data
  shape = numpy.shape(data)                          # guardo el shape original de data
  data_vector = numpy.reshape(data,numpy.size(data)) # genero un vector de data usando su size (largo*ancho)
  # data_vector = calibrarData(band, data_vector)      # invoco la funcion sobre el vector
  
  # i = 0
  # while i < numpy.size(data):
  #   if math.isnan(data_vector[i]):
  #     data_vector[i] = 0.
  #   i += 1

  data = numpy.reshape(data_vector, shape)            # paso el vector a matriz usando shape como largo y ancho

  print numpy.size(data)

  # print img[56][85]
  print lats[56]
  print lons[85]

  for i in data:
    for j in i:
      if not math.isnan(j):
        print j

  print "min: " + str(numpy.amin(lats)) + ", " + str(numpy.amin(lons))
  print "max: " + str(numpy.amax(lats)) + ", " + str(numpy.amax(lons))

  print numpy.amin(data)
  print numpy.amax(data)

  # dadas las lat y lon del archivo, obtengo las coordenadas x y para
  # la ventana seleccionada como proyeccion
  # x, y = ax1(lons,lats)
  # x = lons
  # y = lats
  # x, y = numpy.meshgrid(lons,lats)

  lons2d, lats2d = numpy.meshgrid(lons, lats)
  # y luego obtengo sus coordenadas en el mapa ax
  x, y = ax1(lons2d,lats2d)

  # vmin=1.
  # vmax=10.

  vmin = numpy.amin(data)
  vmax = numpy.amax(data)

  # data = numpy.array(data)
  data = numpy.ma.masked_where(numpy.isnan(data), data)

  # dibujo img en las coordenadas x e y calculadas
  # cs = ax1.pcolormesh(x, y, img, vmin=0., vmax=vmax, cmap='jet')

  cmap = gmtColormap('GHIscale','/home/ldovat/netcdf',1100)
  cs   = ax1.pcolormesh(x, y, data, vmin=vmin, vmax=vmax, cmap=cmap)

  # agrego los vectores de las costas, departamentos/estados/provincias y paises
  # ax1.drawcoastlines()
  # ax1.drawstates()
  # ax1.drawcountries()

  # dibujo los valores de latitudes y longitudes
  # ax1.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10)
  # ax1.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10)

  # agrego el colorbar
  cbar = ax1.colorbar(cs, location='bottom', pad='3%', ticks=[vmin, vmax])
  # cbar.ax.set_xticklabels([vmin, vmax], fontsize=10)

  name     = basename(url)           # obtengo el nombre base del archivo
  destFile = dirDest + name + '.png' # determino el nombre del archivo a escribir

  plt.savefig(destFile, bbox_inches='tight', dpi=200, transparent=True) #, transparent=True
  plt.close()

# def netcdf2png

url     = '/home/ldovat/netcdf/MSUv2_GHI_anual_2m.nc'
dirDest = '/home/ldovat/netcdf/'

ncdump(url)
print '------------------------'
netcdf2png(url, dirDest)
