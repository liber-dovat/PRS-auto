#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import netCDF4
import numpy
import datetime
import os
from os.path import basename
import matplotlib.gridspec as gridspec
from funciones import ymd

def ncdump(nc_fid, verb=True):
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

def netcdf2png(url, dirDest):
  
  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')
                                          
  # extract/copy the data
  lats    = nc_fid.variables['lat'][:]
  lons    = nc_fid.variables['lon'][:]
  data    = nc_fid.variables['data'][:]

  nc_fid.close()

  lon_0 = lons.mean()
  lat_0 = lats.mean()

  # gs = gridspec.GridSpec(2, 1, height_ratios=[18,1])
  # ax1 = plt.subplot(gs[0])

              # llcrnrlat=-48.45835,urcrnrlat=-13.9234,\
              # llcrnrlon=-71.10352,urcrnrlon=-40.16602,\
              # llcrnrlat=-41.260204,urcrnrlat=-27.534344,\
              # llcrnrlon=-67.620302,urcrnrlon=-45.384947,\
              # llcrnrlat=-45.500000,urcrnrlat=-21.476581,\
              # llcrnrlon=-69.358537,urcrnrlon=-30.840110,\
              # llcrnrlat=-42.962770,urcrnrlat=-21.898679,\
              # llcrnrlon=-66.826158,urcrnrlon=-44.968092,\
  ax1 = Basemap(projection='merc',lon_0=lon_0,lat_0=lat_0,\
              llcrnrlat=-42.866693,urcrnrlat=-22.039758,\
              llcrnrlon=-66.800000,urcrnrlon=-44.968092,\
              resolution='h')

  img = data[0]

  # dadas las lat y lon del archivo, obtengo las coordenadas x y para
  # la ventana seleccionada como proyeccion
  x,y = ax1(lons,lats)

  # cm le define el esquema de colores
  # https://gist.github.com/endolith/2719900
  ax1.pcolormesh(x, y, img)

  ax1.drawcoastlines()
  ax1.drawstates()
  ax1.drawcountries()

  plt.axis('off')

  # Probar la marca de agua como un subplot 
  # http://ramiro.org/notebook/matplotlib-branding/
  watermark = plt.imread('/sat/PRS/libs/PRS-auto/imgs/les-logo.png')
  plt.figimage(watermark, 6, 10)

  # subplots(figsize=(18, 2))
  # http://stackoverflow.com/questions/13384653/imshow-extent-and-aspect
  # http://stackoverflow.com/questions/24185083/change-resolution-of-imshow-in-ipython

  # ax2 = plt.subplot(gs[1])
  # ax2.imshow(watermark)
  # ax2.axis('off')
  # ax2.figure.set_figheight(4)

  name = basename(url)
  destFile = dirDest + name + '.png'
  name_split = name.split(".")[1:4]
  month = ymd(int(name_split[0]), int(name_split[1]))
  name_split.insert(1, str(month[1]).zfill(2))
  plt.annotate(name.split(".")[4] + ' ' + '.'.join(name_split), (0,0), (40, -10), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=10, family='monospace')
  plt.savefig(destFile, bbox_inches='tight', dpi=200)
  plt.close()

# def netcdf2png

# netcdf2png('./imagen/goes13.2016.265.160732.BAND_04.nc','./png/')
# netcdf2png('./imagen/goes13.2016.265.160732.BAND_06.nc','./png/')
