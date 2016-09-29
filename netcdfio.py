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

  if banda == "BAND_01":
    return "CH1 FR"
  elif banda == "BAND_02":
    return "CH2 T2"
  elif banda == "BAND_03":
    return "CH3 T3"
  elif banda == "BAND_04":
    return "CH4 T4"
  elif banda == "BAND_06":
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
  lats    = nc_fid.variables['lat'][:]
  lons    = nc_fid.variables['lon'][:]
  data    = nc_fid.variables['data'][:]

  nc_fid.close()

  lon_0 = lons.mean()
  lat_0 = lats.mean()

  ax1 = Basemap(projection='merc',lon_0=lon_0,lat_0=lat_0,\
              llcrnrlat=-42.866693,urcrnrlat=-22.039758,\
              llcrnrlon=-66.800000,urcrnrlon=-44.968092,\
              resolution='l')

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
  name       = basename(url)           # obtengo el nombre base del archivo
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
  str_chnl  = nameTag(name.split(".")[4])

  tag = str_chnl + " " + str_day + "-" + str_month + "-" + year + " " + str_hm + " UTC"

  # agego el pie de pagina usando annotate
  plt.annotate(tag, (0,0), (140, -50), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=10, family='monospace')
  plt.savefig(destFile, bbox_inches='tight', dpi=200)
  plt.close()

# def netcdf2png
