#!/usr/bin/python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import netCDF4
import numpy
import datetime

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

def netcdf2png(url):

  file = netCDF4.Dataset(url,'r')

  # examine the variables
  print file.variables.keys()
  # print file.variables['z']

  lon        = file.variables['lon'][:]
  lat        = file.variables['lat'][:]
  time       = file.variables['time'][:]
  dataWidth  = file.variables['dataWidth'][:]
  lineRes    = file.variables['lineRes'][:]

  lon_u      = file.variables['lon'].units
  lat_u      = file.variables['lat'].units
  time_u     = file.variables['time'].units
  lineRes_u  = file.variables['lineRes'].units

  print lon
  print lon_u
  print lat
  print lat_u
  print time
  print time_u
  print dataWidth
  print lineRes
  print lineRes_u

  print lon.size
  print lon.shape

  print lat_u.size
  print lat.shape

  file.close()

# def netcdf2png

#########################################
#########################################
#########################################
#################################### Main

archivo = './imagen/goes13.2016.251.140733.BAND_04.nc'

# Dataset is the class behavior to open the file
# and create an instance of the ncCDF4 class
nc_fid = netCDF4.Dataset(archivo, 'r')
                                        
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

lats = nc_fid.variables['lat'][:]  # extract/copy the data
lons = nc_fid.variables['lon'][:]
data = nc_fid.variables['data'][:]
lineRes = nc_fid.variables['lineRes'][:]
elemRes = nc_fid.variables['elemRes'][:]

nc_fid.close()

lon_0 = lons.mean()
lat_0 = lats.mean()

print lon_0
print lat_0

#                low left                  upper right
print "Lats: " + str(lats[-1][-1]) + "," + str(lats[0][0])
print "Lons: " + str(lons[0][0])   + "," + str(lons[-1][-1])

            # llcrnrlat=-48.45835,urcrnrlat=-13.9234,\
            # llcrnrlon=-71.10352,urcrnrlon=-40.16602,\
            # llcrnrlat=-41.260204,urcrnrlat=-27.534344,\
            # llcrnrlon=-67.620302,urcrnrlon=-45.384947,\
            # llcrnrlat=-45.783816,urcrnrlat=-21.476581,\
            # llcrnrlon=-65.811160,urcrnrlon=-30.840110,\
m = Basemap(projection='merc',lon_0=lon_0,lat_0=lat_0,\
            llcrnrlat=-45.783816,urcrnrlat=-21.476581,\
            llcrnrlon=-65.811160,urcrnrlon=-30.840110,\
            resolution='h')

img = data[0]

# dadas las lat y lon del archivo, obtengo las coordenadas x y para
# la ventana seleccionada como proyeccion
x,y = m(lons,lats)

# cm le define el esquema de colores
# m.imshow(img, cm.GMT_haxby)
# https://gist.github.com/endolith/2719900
m.pcolormesh(x, y, img)

m.drawcoastlines()
m.drawstates()
m.drawcountries()

plt.axis('off')
plt.savefig(archivo+str(datetime.datetime.now())+'.png', bbox_inches=0, dpi=200)
# plt.show()
