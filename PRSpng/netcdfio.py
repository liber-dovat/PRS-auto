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
from multiprocessing import Pool
from functools import partial

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

# http://matplotlib.org/users/colormapnorms.html
# http://stackoverflow.com/questions/35295075/define-custom-normalisation-function-in-matplotlib-when-using-plt-colorbar

'''
Custom colormap
'''

class colormapInfrarrojo(colors.Normalize):
  def __init__(self, vmin=None, vmax=None, clip=False):
    colors.Normalize.__init__(self, vmin, vmax, clip)

  def __call__(self, value, clip=None):
    # I'm ignoring masked values and all kinds of edge cases to make a
    # simple example...
    norma = [0, 40, 80, 118, 158, 197, 236, 276, 316, 354, 394, 1024]
    return numpy.ma.masked_array(numpy.interp(value, norma, norma))

#########################################
#########################################
#########################################
'''
# http://stackoverflow.com/questions/24004887/matplotlib-pcolormesh-separate-datacolor-and-color-brightness-information
def mapeoColorInfrarrojo(valor):

  i01 = 40;
  i02 = 80;
  i03 = 118;
  i04 = 158;
  i05 = 197;
  i06 = 236;
  i07 = 276;
  i08 = 316;
  i09 = 354;
  i10 = 394;
  iT  = 1024;

  C1 = 0.85;
  C2 = 0.15;

  map = zeros(iT, 3);

  # COLORES CON CODIGO
  if valor in range(1,i01)
     return [0 0 0]
  end
  for k=(i01+1:i02)
     map(k,:) = [153 0 0]/255; 
  end
  for k=(i02+1:i03)
     map(k,:) = [153 0 153]/255; 
  end
  for k=(i03+1:i04)
     map(k,:) = [255 0 0]/255; 
  end
  for k=(i04+1:i05)
     map(k,:) = [255 102 0]/255;
  end
  for k=(i05+1:i06)
     map(k,:) = [255 255 0]/255;
  end
  for k=(i06+1:i07)
     map(k,:) = [0 153 0]/255;
  end
  for k=(i07+1:i08)
     map(k,:) = [0 255 0]/255;
  end
  for k=(i08+1:i09)
     map(k,:) = [0 0 255]/255;
  end
  for k=(i09+1:i10)
     map(k,:) = [0 153 153]/255;
  end
   # ESCALA DE GRISES
  for k=(i10+1:iT)
      Ik = (C1-C2)*((k-iT)/(i10+1-iT)) + C2;
      map(k,:) = [Ik Ik Ik]; 
  end
# mapeoColorInfrarrojo
'''
#########################################
#########################################
#########################################

# http://stackoverflow.com/questions/11442191/parallelizing-a-numpy-vector-operation
# leer para paralelizar
# http://www.star.nesdis.noaa.gov/smcd/spb/fwu/homepage/GOES_Imager_Vis_OpCal_G13.php
# Correccion de muestras

# Rpre  = (dato - b)/m
# C = alfa * exp(beta * dt)
# Rpost = Rpre * C

def Radiance(dato,m,b):
  return (dato - b)/m
# Radiance

#########################################
#########################################
#########################################

def temperaturaReal(dato,m,b1,n,a,b2):
  c1 = 1.191066e-5
  c2 = 1.438833

  lx   = (dato - b1) / m
  aux  = 1 + ( (c1*numpy.power(n, 3)) / lx )
  Teff = (c2*n) / numpy.log(aux)
  Temp = a + b2 * Teff

  return Temp
# temperaturaReal

#########################################
#########################################
#########################################

def normalizarData(banda, data):

  # seteo las variables en funcion de las bandas
  if banda == 1:
    m = 227.3889
    b = 68.2167
  elif banda == 2:
    m  = 227.3889
    b1 = 68.2167
    n  = 2561.74
    a  = -1.437204
    b2 = 1.002562
  elif banda == 3:
    m  = 38.8383
    b1 = 29.1287
    n  = 1522.52
    a  = -3.625663
    b2 = 1.010018
  elif banda == 4:
    m  = 5.2285
    b1 = 15.6854
    n  = 937.23
    a  = -0.386043
    b2 = 1.001298
  elif banda == 6:
    m  = 5.5297
    b1 = 16.5892
    n  = 749.83
    a  = -0.134801
    b2 = 1.000482

  # aplico la funcion como un map en cada elemento
  if banda == 1:
    return Radiance(data,m,b)
  else:
    vfunc = numpy.vectorize(temperaturaReal)
    return vfunc(data,m,b1,n,a,b2)

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

  data = data[0]                                     # me quedo con el primer elemento de data
  shape = numpy.shape(data)                          # guardo el shape original de data
  data_vector = numpy.reshape(data,numpy.size(data)) # genero un vector de data usando su size (largo*ancho)
  data_vector = normalizarData(band, data_vector)    # invoco la funcion sobre el vector
  img = numpy.reshape(data_vector, shape)            # paso el vector a matriz usando shape como largo y ancho

  if band != 1:
    img *= 1.0/numpy.amax(img)

  print numpy.amin(img)
  print numpy.amax(img)

  # if band == 4:
  #   plt.plot(data_vector[0:1000])
  #   plt.show()
  #   plt.savefig("./test/img0_1000.png", bbox_inches='tight', dpi=200)

  # dadas las lat y lon del archivo, obtengo las coordenadas x y para
  # la ventana seleccionada como proyeccion
  x, y = ax1(lons,lats)

  if band == 1:
    vmax=100.
  else:
    vmax=1.0/numpy.amax(img)

  # dibujo img en las coordenadas x e y calculadas
  # cs = ax1.pcolormesh(x, y, img, vmin=0., vmax=vmax, cmap='jet')
  if band == 1:
    cs = ax1.pcolormesh(x, y, img, vmin=0., vmax=vmax, cmap='jet')
  else:
    cs = ax1.pcolormesh(x, y, img, vmin=0., vmax=vmax, cmap='jet', norm=colormapInfrarrojo())

  # agrego los vectores de las costas, departamentos/estados/provincias y paises
  ax1.drawcoastlines()
  ax1.drawstates()
  ax1.drawcountries()

  # dibujo los valores de latitudes y longitudes
  ax1.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10)
  ax1.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10)

  # agrego el colorbar
  cbar = ax1.colorbar(cs, location='bottom', pad='3%', ticks=[0., vmax])
  cbar.ax.set_xticklabels(['0', vmax], fontsize=10)

  # agrego el logo en el documento
  logo = plt.imread('/sat/PRS/libs/PRS-auto/PRSpng/imgs/les-logo.png')
  plt.figimage(logo, 5, 5)

  # genero los datos para escribir el pie de pagina
  name     = basename(url)           # obtengo el nombre base del archivo
  destFile = dirDest + name + '.png' # determino el nombre del archivo a escribir
  
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
