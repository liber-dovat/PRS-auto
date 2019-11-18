#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import datetime
import netCDF4
import numpy
import os
import re

from mpl_toolkits.basemap import Basemap
from pyproj               import Proj
from utils                import gmtColormap
from shutil               import copyfile
from matplotlib.patches   import Polygon
from funciones            import cosSolarZenithAngle, FnFunc

#########################################
#########################################
#########################################

def rincon_de_artigas_poly(m):
  lats = [-30.858550,-30.957062,-31.000216,-31.040658]
  lons = [-55.979755,-55.912115,-55.842423,-55.820785]

  x, y = m( lons, lats )
  xy   = zip(x,y)
  poly = Polygon( list(xy), closed=False, edgecolor='k', linewidth=0.4, facecolor='none', fill=False)
  plt.gca().add_patch(poly)

#########################################
#########################################
#########################################

def truncUno(d):
  if d > 1: return 1
# end truncUno

#########################################
#########################################
#########################################

def setcolor(x, color):
  for m in x:
    for t in x[m][1]:
      t.set_color(color)

#########################################
#########################################
#########################################

def fr2ghi2png(url, colormapPath, colormapName, dirDest, lat_name, lon_name, data_name, geos=False):
  
  # Dataset is the class behavior to open the file
  # and create an instance of the ncCDF4 class
  nc_fid = netCDF4.Dataset(url, 'r')

  t_coverage = repr(nc_fid.getncattr('time_coverage_start'))
  # print t_coverage

  ds_name = repr(nc_fid.getncattr('dataset_name'))
  # print ds_name

  date = re.search('\'(.*?)\'', t_coverage).group(1)
  print(date)

  channel = re.search('-M\d(.*?)_', ds_name).group(1)
  print(channel)

  yl = date[0:4]
  yy = date[2:4]
  mt = date[5:7]
  dd = date[8:10]
  hh = date[11:13]
  mm = date[14:16]
  ss = date[17:19]

  str_date = str(dd) + '/' + str(mt) + '/' + str(yl) + " " + str(hh) + ":" + str(mm)
  date     = datetime.datetime.strptime(str_date, '%d/%m/%Y %H:%M') - datetime.timedelta(hours=3)
  name     = channel + " " + date.strftime('%d-%m-%Y %H:%M')
  filename = channel + "_" + yy + mt + dd + "_" + hh + mm + ss
  # print "name: " + name

  # extract/copy the data
  data = nc_fid.variables[data_name][:]

  if data_name == 'CMI' or data_name == 'Rad':
    # Satellite height
    sat_h = nc_fid.variables['goes_imager_projection'].perspective_point_height
    # Satellite longitude
    sat_lon = nc_fid.variables['goes_imager_projection'].longitude_of_projection_origin
    # Satellite sweep
    sat_sweep = nc_fid.variables['goes_imager_projection'].sweep_angle_axis
    X = nc_fid.variables[lon_name][:] # longitud, eje X
    Y = nc_fid.variables[lat_name][:] # latitud, eje Y

    scene_id_val = repr(nc_fid.getncattr('scene_id'))
    scene_id     = re.search('\'(.*?)\'', scene_id_val).group(1)

  nc_fid.close()

  print("Realizando pasaje a K en C13 y truncamiento en los otros")

  for d in numpy.nditer(data, op_flags=['readwrite']):
    d = truncUno(d)
  data *= 100

  #######################################
  #######################################

  name = "GHI " + date.strftime('%d-%m-%Y %H:%M')


  nc_fid_ghi = netCDF4.Dataset(url, 'r')

  data = nc_fid_ghi.variables[data_name][:]
  X    = nc_fid_ghi.variables[lon_name][:] # longitud, eje X
  Y    = nc_fid_ghi.variables[lat_name][:] # latitud, eje Y
  nc_fid_ghi.close()

  for d in numpy.nditer(data, op_flags=['readwrite']):
    d = truncUno(d)
  data *= 100

  X *= sat_h
  Y *= sat_h

  vmin = 0.0
  vmax = 1200.0

  ax = Basemap(projection='merc',\
      llcrnrlat=-35.00,urcrnrlat=-30.00,\
      llcrnrlon=-58.77,urcrnrlon=-53.00,\
      resolution='f')
  projection = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep, ellps='WGS84')

  x_mesh, y_mesh = numpy.meshgrid(X,Y)
  lons, lats     = projection(x_mesh, y_mesh, inverse=True)
  x, y           = ax(lons, lats)

  ax.drawcoastlines(linewidth=0.40)
  ax.drawcountries(linewidth=0.40)
  ax.drawstates(linewidth=0.20)

  rincon_de_artigas_poly(ax)

  par = ax.drawparallels(numpy.arange(-40, -20, 2), labels=[1,0,0,0], linewidth=0.0, fontsize=7, color='white')
  mer = ax.drawmeridians(numpy.arange(-70, -40, 2), labels=[0,0,1,0], linewidth=0.0, fontsize=7, color='white')
  setcolor(par,'white')
  setcolor(mer,'white')

  print("Calculando GHI...")

  Isc = 1367.0
  # JPTv1
  a   = 0.602
  b   = 0.576
  c   = -0.341
  d   = -13.149

  def FR2GHI(lat, lon, fr):
    Cz, Gamma = cosSolarZenithAngle(lat, lon, date, 0)
    ghi = 0.
    if Cz > 0.:
      Fn = FnFunc(Gamma)
      ghi = Isc*Fn*Cz*(a+b*Cz+c*Cz)+d*fr
      if Isc*Fn*Cz != 0:
        Kt = ghi/(Isc*Fn*Cz)
        Kt = numpy.clip(Kt,0.09,0.85)
      ghi = Kt*Isc*Fn*Cz
    return ghi
  FR2GHI_vect = numpy.vectorize(FR2GHI, otypes=[float])

  GHI = FR2GHI_vect(lats, lons, data)

  ticks =  [0, 200, 400, 600, 800, 1000, 1200]
  ticksLabels = ticks

  cmap = gmtColormap('irradiancia_v6', colormapPath, 2048)
  cs   = ax.pcolormesh(x, y, GHI, vmin=vmin, vmax=vmax, cmap=cmap)

  plt.clim(vmin, vmax)

  # agrego el colorbar
  cbar = ax.colorbar(cs, location='bottom', ticks=ticks) # , pad='3%'
  cbar.ax.set_xlabel("Irradiancia solar global en plano horizontal ($W/m^2$)", fontsize=7, color='white')
  cbar.ax.set_xticklabels(ticksLabels, fontsize=7, color='white')

  # agrego el logo en el documento
  logo_bw = plt.imread('/sat/PRS/dev/PRS-sat/PRSgoes/logo_300_bw.png')
  plt.figimage(logo_bw, xo=5, yo=5)

  if not os.path.isdir(dirDest + channel + '/' + yl + '/ghi'):
    os.mkdir(dirDest + channel + "/" + yl + '/ghi')
  # if

  outPath = dirDest + channel + "/" + yl + "/ghi/"

  whitePath = outPath + filename + '_ghi_white.png' # determino el nombre del archivo a escribir
  outPath   = outPath + filename + '_ghi.png' # determino el nombre del archivo a escribir

  x_coord = 109
  y_coord = -53

  Noche = numpy.sum(data) <= 0.

  if Noche: # print "es noche"
    plt.annotate("NOCHE", (0,0), (204, 15), color='white', xycoords='axes fraction', textcoords='offset points', va='top', fontsize=10, family='monospace')

  plt.annotate(name + " UY", (0,0), (x_coord, y_coord), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=11, family='monospace', color='white')
  plt.savefig(outPath, bbox_inches='tight', dpi=400, transparent=True) # , facecolor='#4F7293'

  cbar.ax.set_xlabel("Irradiancia solar global en plano horizontal ($W/m^2$)", fontsize=7, color='black')
  cbar.ax.set_xticklabels(ticksLabels, fontsize=7, color='black')

  # WHITE

  setcolor(par,'black')
  setcolor(mer,'black')

  logo_color = plt.imread('/sat/PRS/dev/PRS-sat/PRSgoes/logo_300_color.png')
  plt.figimage(logo_color, xo=5, yo=5)

  nota_ghi_w = plt.annotate(name + " UY", (0,0), (x_coord, y_coord), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=11, family='monospace', color='black')
  plt.savefig(whitePath, bbox_inches='tight', dpi=400, transparent=False , facecolor='white') # , facecolor='#4F7293'

  copyfile(outPath,   dirDest + channel + '_ghi.png')
  copyfile(whitePath, dirDest + channel + '_ghi_white.png')

  print("NUBOSIDAD")
  # NUBOSIDAD

  plt.clf()

  ax.drawcoastlines(linewidth=0.40)
  ax.drawcountries(linewidth=0.40)
  ax.drawstates(linewidth=0.20)

  rincon_de_artigas_poly(ax)

  par = ax.drawparallels(numpy.arange(-40, -20, 2), labels=[1,0,0,0], linewidth=0.0, fontsize=7, color='white')
  mer = ax.drawmeridians(numpy.arange(-70, -40, 2), labels=[0,0,1,0], linewidth=0.0, fontsize=7, color='white')
  setcolor(par,'white')
  setcolor(mer,'white')

  vmin = 0.0
  vmax = 100.0

  ticks       = [0, 20, 40, 60, 80, 100]
  ticksLabels = ticks

  cmap = gmtColormap('nubosidad', colormapPath, 2048)
  cs   = ax.pcolormesh(x, y, data, vmin=vmin, vmax=vmax, cmap=cmap)

  plt.clim(vmin, vmax)

  # agrego el colorbar
  cbar = ax.colorbar(cs, location='bottom', ticks=ticks) # , pad='3%'
  cbar.ax.set_xlabel("Nubosidad (%)", fontsize=7, color='white')
  cbar.ax.set_xticklabels(ticksLabels, fontsize=7, color='white')

  plt.figimage(logo_bw, xo=5, yo=5)

  outPath = dirDest + channel + "/" + yl + "/ghi/"

  outPath   = outPath + filename + '_cloud.png' # determino el nombre del archivo a escribir
  whitePath = outPath + filename + '_cloud_white.png' # determino el nombre del archivo a escribir

  x_coord = 109
  y_coord = -53

  plt.annotate("C02 " + date.strftime('%d-%m-%Y %H:%M') + " UY", (0,0), (x_coord, y_coord), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=11, family='monospace', color='white')
  plt.draw()
  plt.savefig(outPath, bbox_inches='tight', dpi=400, transparent=True) # , facecolor='#4F7293'

  # CLOUD WHITE

  setcolor(par,'black')
  setcolor(mer,'black')

  logo_color = plt.imread('/sat/PRS/dev/PRS-sat/PRSgoes/logo_300_color.png')
  plt.figimage(logo_color, xo=5, yo=5)

  plt.annotate("C02 " + date.strftime('%d-%m-%Y %H:%M') + " UY", (0,0), (x_coord, y_coord), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=11, family='monospace', color='black')
  plt.savefig(whitePath, bbox_inches='tight', dpi=400, transparent=False , facecolor='white') # , facecolor='#4F7293'

  copyfile(outPath, dirDest + channel + '_cloud.png')
  copyfile(whitePath, dirDest + channel + '_cloud_white.png')

  plt.close()

# def netcdf2png
