import matplotlib
matplotlib.use('Agg')
from matplotlib import colors
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import netCDF4
import numpy
import datetime
import os
from os.path import basename
from funciones import ymd
import math

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

def nameTag(banda):

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

def temperaturaReal(m,b,n,alfa,beta,dato):
  c1 = 1.191066e-5
  c2 = 1.438833

  R = (dato - b)/m
  Teff = (c2*n) / math.log(1 + (c1*math.pow(n, 3) / R))
  Temp = alfa + beta * Teff
  return Temp
# temperaturaReal

#########################################
#########################################
#########################################

def normalizarData(banda, data):

  if banda == 1:
    m = 227.3889
    b = 68.2167
    new_data = [(dato - b)/m for dato in data]
  elif banda == 2:
    m = 227.3889
    b = 68.2167
    n = 2561.74
    alfa = -1.437204
    beta = 1.002562
    new_data = [temperaturaReal(m,b,n,alfa,beta,dato) for dato in data]
  elif banda == 3:
    m = 38.8383
    b = 29.1287
    n = 1522.52
    alfa = -3.625663
    beta = 1.010018
    new_data = [temperaturaReal(m,b,n,alfa,beta,dato) for dato in data]
  elif banda == 4:
    m = 5.2285
    b = 15.6854
    n = 937.23
    alfa = -0.386043
    beta = 1.001298
    new_data = [temperaturaReal(m,b,n,alfa,beta,dato) for dato in data]
  elif banda == 6:
    m = 5.5297
    b = 16.5892
    n = 749.83
    alfa = -0.134801
    beta = 1.000482
    new_data = [temperaturaReal(m,b,n,alfa,beta,dato) for dato in data]

  return new_data

# normalizarData

#########################################
#########################################
#########################################

def netcdf2png(url, dirDest):
  
  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')

  # extract/copy the data
  lats = nc_fid.variables['lat'][:]
  lons = nc_fid.variables['lon'][:]
  data = nc_fid.variables['data'][:]
  band = nc_fid.variables['bands'][:]

  nc_fid.close()

  lon_0 = lons.mean()
  lat_0 = lats.mean()

  ax1 = Basemap(projection='merc',lon_0=lon_0,lat_0=lat_0,\
              llcrnrlat=-42.866693,urcrnrlat=-22.039758,\
              llcrnrlon=-66.800000,urcrnrlon=-44.968092,\
              resolution='l')

  # img = normalizarData(band, data[0])

  # data = data[0]
  # shape = numpy.shape(data)
  # data_vector = numpy.reshape(data,numpy.size(data))
  # data_vector = normalizarData(band, data_vector)
  # img = numpy.reshape(data_vector, shape)

  img = data[0]
  img *= 1024.0/numpy.amax(img) # normalizo los datos desde cero hasta 1024

  # http://matplotlib.org/users/colormapnorms.html

  # dadas las lat y lon del archivo, obtengo las coordenadas x y para
  # la ventana seleccionada como proyeccion
  x, y = ax1(lons,lats)

  # dibujo img en las coordenadas x e y calculadas
  cs = ax1.pcolormesh(x, y, img, vmin=0., vmax=1024., cmap='jet')
  # ax1.pcolormesh(x, y, img, cmap='jet')

  # agrego los vectores de las costas, departamentos/estados/provincias y paises
  ax1.drawcoastlines()
  ax1.drawstates()
  ax1.drawcountries()

  # dibujo los valores de latitudes y longitudes
  ax1.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10)
  ax1.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10)

  # agrego el colorbar
  cbar = ax1.colorbar(cs, location='bottom', pad='3%', ticks=[0., 512., 1024.])
  cbar.ax.set_xticklabels(['Low', 'Medium', 'High'], fontsize=10)

  # agrego el logo en el documento
  logo = plt.imread('/sat/PRS/libs/PRS-auto/imgs/les-logo.png')
  plt.figimage(logo, 5, 5)

  # genero los datos para escribir el pie de pagina
  name  = basename(url)                # obtengo el nombre base del archivo
  destFile   = dirDest + name + '.png' # determino el nombre del archivo a escribir
  
  name_split = name.split(".")[1:4]
  year       = name_split[0]
  doy        = name_split[1]
  hms        = name_split[2]
  month      = ymd(int(year), int(doy))[1]
  day        = ymd(int(year), int(doy))[2]

  str_day   = str(day).zfill(2)
  str_month = str(month).zfill(2)
  str_hm    = hms[0:2] + ":" +hms[2:4]
  str_chnl  = nameTag(band)

  tag = str_chnl + " " + str_day + "-" + str_month + "-" + year + " " + str_hm + " UTC"

  # agego el pie de pagina usando annotate
  plt.annotate(tag, (0,0), (140, -50), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=10, family='monospace')
  plt.savefig(destFile, bbox_inches='tight', dpi=200)
  plt.close()

# def netcdf2png
