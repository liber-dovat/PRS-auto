#!/usr/bin/python
# -*- coding: utf-8 -*-

import netCDF4
import numpy
from mpl_toolkits.basemap import Basemap
from pyproj               import Proj

def getCutCells(url, lat_name, lon_name, estaciones, lat_offset, lon_offset):

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

  print(len(x))
  print(len(x[0]))

  for estacion in estaciones:

    center_lat = estacion[0]
    center_lon = estacion[1]

    print('llcrnrlat=' + str(center_lat - lat_offset) + ',urcrnrlat=' + str(center_lat + lat_offset) + ',\\')
    print('llcrnrlon=' + str(center_lon - lon_offset) + ',urcrnrlon=' + str(center_lon + lon_offset) + ',\\')

    j_less  = len(x)
    j_great = 0

    i_less  = len(y)
    i_great = 0

    for i in range(0,len(x)):      # recorro verticalmente
      for j in range(0,len(x[0])): # recorro horizontalmente
        if (x[i][j] > center_lon - lon_offset) and\
           (x[i][j] < center_lon + lon_offset) and\
           (y[i][j] > center_lat - lat_offset) and\
           (y[i][j] < center_lat + lat_offset):
          if j < j_less:
            j_less = j
          if j > j_great:
            j_great = j

          if i < i_less:
            i_less = i
          if i > i_great:
            i_great = i

    # print 'j_less = ' + str(j_less)
    # print 'j_great= ' + str(j_great)
    # print 'i_less = ' + str(i_less)
    # print 'i_great= ' + str(i_great)

    # return j_less, j_great, i_less, i_great
    print(estacion[4])
    print('ncks -d x,%d,%d -d y,%d,%d <in> -O <out>_%s.nc' % (j_less, j_great, i_less, i_great, estacion[3]))
    print("")

  # for

# def netcdf2png

#########################################
#########################################
#########################################

ncpath = '/sat/PRS/dev/PRS-sat/PRSgoes/cut/'
files  = ['band02M3_G16_s20180731300_noaa.nc']

estaciones = [
[  -15.5553,  -56.07000,  185, "cui", "Cuiabá"],\
[  -15.6000,  -47.71300, 1023, "bra", "Brasilia"],\
[  -10.1778,  -48.36190,  216, "pal", "Palmas"],\
[   -9.0689,  -40.31970,  387, "pet", "Petrolina "],\
[   -2.5933,  -44.21220,   40, "slu", "São Luís"],\
[   -6.4669,  -37.08470,  176, "cai", "Caiocó"],\
[   -5.8367,  -35.20640,   58, "nat", "Natal"],\
[ +40.05192,  -88.37309,  230, "bnd", "Bondville, Illinois, UTC+6"],\
[ +40.12498, -105.23680, 1689, "tbl", "Table Mountain, Boulder, Colorado, UTC+7"],\
[ +36.62373, -116.01947, 1007, "dra", "Desert Rock, Nevada, UTC+8"],\
[ +48.30783, -105.10170,  634, "fpk", "Fort Peck, Montana, UTC+7"],\
[ +34.25470,  -89.87290,   98, "gwn", "Goodwin Creek, Mississippi, UTC+6"],\
[ +40.72012,  -77.93085,  376, "psu", "Penn. State Univ., UTC+5"],\
[ +43.73403,  -96.62328,  473, "sxf", "Sioux Falls, South Dakota, UTC+6"],\
[ +16.21700,  -61.51700,    6, "fol", "Pointe à Pitre (Fouillole)"],\
[ +35.03800, -106.62210, 1617, "alb", "Albuquerque"],\
] # estaciones

getCutCells(ncpath + files[0], 'y', 'x', estaciones, 1.0, 1.0)
