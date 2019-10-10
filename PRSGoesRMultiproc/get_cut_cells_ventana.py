#!/usr/bin/python
# -*- coding: utf-8 -*-

import netCDF4
import numpy
from mpl_toolkits.basemap import Basemap
from pyproj               import Proj

def getCutCells(url, lat_name, lon_name, lat_max, lat_min, lon_max, lon_min):

  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')

  sat_h     = nc_fid.variables['goes_imager_projection'].perspective_point_height
  sat_lon   = nc_fid.variables['goes_imager_projection'].longitude_of_projection_origin
  sat_sweep = nc_fid.variables['goes_imager_projection'].sweep_angle_axis

  X = nc_fid.variables[lon_name][:] # longitud, eje X
  Y = nc_fid.variables[lat_name][:] # latitud,  eje Y

  nc_fid.close()

  X *= sat_h
  Y *= sat_h

  x_mesh, y_mesh = numpy.meshgrid(X,Y)
  proj_string = "+proj=geos +h=" + str(sat_h) + " +lon_0=" + str(sat_lon) + " +sweep=" + str(sat_sweep) + " +ellps=WGS84"
  projection = Proj(proj_string)
  x, y = projection(x_mesh, y_mesh, inverse=True)

  print len(x)
  print len(x[0])

  # print 'llcrnrlat=' + str(center_lat - lat_offset) + ',urcrnrlat=' + str(center_lat + lat_offset) + ',\\'
  # print 'llcrnrlon=' + str(center_lon - lon_offset) + ',urcrnrlon=' + str(center_lon + lon_offset) + ',\\'

  j_less  = len(x)
  j_great = 0

  i_less  = len(y)
  i_great = 0

  for i in range(0,len(x)):      # recorro verticalmente
    for j in range(0,len(x[0])): # recorro horizontalmente
      if (x[i][j] > lon_min) and\
         (x[i][j] < lon_max) and\
         (y[i][j] > lat_min) and\
         (y[i][j] < lat_max):
        if j < j_less:
          j_less = j
        if j > j_great:
          j_great = j

        if i < i_less:
          i_less = i
        if i > i_great:
          i_great = i

  print('ncks -d x,%d,%d -d y,%d,%d <in> -O <out>_file.nc' % (j_less, j_great, i_less, i_great))
  print ""

# def netcdf2png

#########################################
#########################################
#########################################

# ncks -d x,11157,17027 -d y,14623,19055 <in> -O <out>_file.nc

ncpath = '/solar/sat/PRS/dev/PRS-sat/PRSGoesRMultiproc/goesr_test/2018/01/C02/'
files  = ['OR_ABI-L2-CMIPF-M3C02_G16_s20180191300388_e20180191311155_c20180191311227.nc']

# -18.00 LATmax   // top    lat
# -43.00 LATmin   // bottom lat
# -43.00 LONmax   // right  lon
# -73.00 LONmin   // left   lon

getCutCells(ncpath + files[0], 'y', 'x', -18.00, -43.00, -43.00, -73.00)
