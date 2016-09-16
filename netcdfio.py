#!/usr/bin/python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4
import numpy

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
  # dataWidth_u = file.variables['dataWidth'].units
  lineRes_u  = file.variables['lineRes'].units

  print lon
  print lon_u
  print lat
  print lat_u
  print time
  print time_u
  print dataWidth
  # print dataWidth_u
  print lineRes
  print lineRes_u

  print lon.size
  print lon.shape

  print lat_u.size
  print lat.shape

  # # sample every 10th point of the 'z' variable
  # topo = file.variables['z'][::10,::10]

  # # make image
  # plt.figure(figsize=(10,10))
  # plt.imshow(topo,origin='lower') 
  # plt.title(file.title)
  # plt.savefig('./imagen/image.png', bbox_inches=0)

  file.close()

# def netcdf2png

#########################################
#########################################
#########################################
#################################### Main

# http://stackoverflow.com/questions/8864599/convert-netcdf-to-image
# http://stackoverflow.com/questions/8864599/convert-netcdf-to-image
# http://www.unidata.ucar.edu/software/netcdf/software.html
# https://code.google.com/archive/p/netcdf4-python/wikis/UbuntuInstall.wiki
# http://www.hydro.washington.edu/~jhamman/hydro-logic/blog/2013/10/12/plot-netcdf-data/

archivo = './imagen/goes13.2016.251.190734.BAND_01.nc'

# Dataset is the class behavior to open the file
# and create an instance of the ncCDF4 class
nc_fid = netCDF4.Dataset(archivo, 'r')
                                        
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

lats = nc_fid.variables['lat'][:]  # extract/copy the data
lons = nc_fid.variables['lon'][:]
data = nc_fid.variables['data'][:]

nc_fid.close()

plt.plot(data)
plt.ylabel('some numbers')
plt.show()

# Get some parameters for the Stereographic Projection
lon_0 = lons.mean()
lat_0 = lats.mean()

# print lon_0
# print lat_0

# m = Basemap(resolution='l',projection='merc',lat_0=lat_0,lon_0=lon_0)

# Because our lon and lat variables are 1D, 
# use meshgrid to create 2D arrays 
# Not necessary if coordinates are already in 2D arrays.
# lon, lat = numpy.meshgrid(lons, lats, sparse=True)
# xi, yi   = m(lon, lat)

# Plot Data
# cs = m.pcolor(xi,yi,data)

# Add Grid Lines
# m.drawparallels(numpy.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
# m.drawmeridians(numpy.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
# m.drawcoastlines()
# m.drawstates()
# m.drawcountries()

# Add Colorbar
# cbar = m.colorbar(cs, location='bottom', pad="10%")

# Add Title
# plt.title('NetCDF Data')
# plt.figure(figsize=(5,5))
# plt.show()
