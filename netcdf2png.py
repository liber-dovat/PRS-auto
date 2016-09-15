#!/usr/bin/python

# http://stackoverflow.com/questions/8864599/convert-netcdf-to-image

import matplotlib.pyplot as plt
import netCDF4

def netcdf2png(url):

  file = netCDF4.Dataset(url)

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

  print lat.size
  print lat.shape

  # # sample every 10th point of the 'z' variable
  # topo = file.variables['z'][::10,::10]

  # # make image
  # plt.figure(figsize=(10,10))
  # plt.imshow(topo,origin='lower') 
  # plt.title(file.title)
  # plt.savefig('./imagen/image.png', bbox_inches=0)

  file.close()

# https://code.google.com/archive/p/netcdf4-python/wikis/UbuntuInstall.wiki
# http://www.hydro.washington.edu/~jhamman/hydro-logic/blog/2013/10/12/plot-netcdf-data/
netcdf2png('./imagen/goes13.2016.251.190734.BAND_01.nc')
 # a, b,c = nfte(url)