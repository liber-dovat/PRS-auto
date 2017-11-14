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
import gc

from mpl_toolkits.basemap import Basemap, shiftgrid
from os.path              import basename
from pyproj               import Proj
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

def netcdf2png(url, colormapPath, colormapName, dirDest, lat_name, lon_name, data_name, geos=False):
  
  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')

  # extract/copy the data
  lats = nc_fid.variables[lat_name][:]
  lons = nc_fid.variables[lon_name][:]
  data = nc_fid.variables[data_name][:]

  if data_name == 'CMI' or data_name == 'DQF':
    # Satellite height
    sat_h = nc_fid.variables['goes_imager_projection'].perspective_point_height
    # Satellite longitude
    sat_lon = nc_fid.variables['goes_imager_projection'].longitude_of_projection_origin
    # Satellite sweep
    sat_sweep = nc_fid.variables['goes_imager_projection'].sweep_angle_axis
    X = nc_fid.variables[lon_name][:] * sat_h # longitud, eje X
    Y = nc_fid.variables[lat_name][:] * sat_h # latitud, eje Y

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
  axes = plt.gca()
  axes.set_xlim([min_lon, max_lon])
  axes.set_ylim([min_lat, max_lat])

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

    ax1 = Basemap(projection='geos', lon_0=sat_lon,\
                  llcrnrx=-x.max()/2,llcrnry=-y.max()/2,\
                  urcrnrx=x.max()/2,urcrnry=y.max()/2,\
                  resolution='l')

  else: # proyecto con mercator en la región del río de la plata

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

    projection = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)

    x_mesh, y_mesh = numpy.meshgrid(X,Y)

    lons, lats = projection(x_mesh, y_mesh, inverse=True)

    # Región
    ax1 = Basemap(projection='merc',\
            llcrnrlat=-42.94,urcrnrlat=-22.0,\
            llcrnrlon=-67.0,urcrnrlon=-45.04,\
            resolution='f')

    # Uruguay
    # ax1 = Basemap(projection='merc',\
    #         llcrnrlat=-35.0830,urcrnrlat=-30.0387,\
    #         llcrnrlon=-58.6475,urcrnrlon=-53.01174,\
    #         resolution='f')

    x, y = ax1(lons, lats)

  # end if

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  vmin = numpy.amin(data)
  # vmin = 250.
  vmax = numpy.amax(data)

  print numpy.amin(data)
  print numpy.amax(data)

  data = numpy.ma.masked_where(numpy.isnan(data), data)

  # dibujo img en las coordenadas x e y calculadas

  cmap = gmtColormap(colormapName,colormapPath, 1100)
  cs = ax1.pcolormesh(x, y, data, vmin=vmin, vmax=vmax, cmap=cmap)

  # cs.set_array(None)

  # seteo los limites del colorbar
  plt.clim(vmin, vmax)

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

  name = basename(url)           # obtengo el nombre base del archivo

  # si estoy dibujando toda la proyección geos adjunto el string al nombre del archivo
  if geos:
    name = name+ "_geos"

  destFile = dirDest + name + '.png' # determino el nombre del archivo a escribir

  # llamo al garbage collector para que borre los elementos que ya no se van a usar
  gc.collect()

  print destFile

  plt.savefig(destFile, bbox_inches='tight', dpi=300, transparent=True) #, transparent=True
  plt.close()

# def netcdf2png
