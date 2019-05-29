#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
# matplotlib.use('Agg')
# matplotlib.use('TkAgg')

import matplotlib.pyplot    as plt
import matplotlib.animation as animation
import sys
import numpy
import math
import time
import glob
import datetime

from os.path              import basename
from mpl_toolkits.basemap import Basemap

#########################################
#########################################
#########################################

def getDate(file):

  base_file = basename(file)
  year = base_file[4:8]
  doy  = base_file[8:11]
  hh   = base_file[12:14]
  mm   = base_file[14:16]
  ss   = base_file[16:18]

  time_data = year + " " + doy + " " + hh  + " " + mm  + " " + ss
  print(time_data)

  date = datetime.datetime.strptime(time_data, '%Y %j %H %M %S')

  return date

#########################################
#########################################
#########################################

def getExt(url):
  name = basename(url)
  return name.split('.')[-1]
# getExt

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

def fileToPng(filesPath, metaPath, point_lat, point_lon, radius):

  # abro el archivo meta y guardo los datos
  fid = open(metaPath + '/T000gri.META', 'r')
  meta = numpy.fromfile(fid, dtype='float32')
  fid.close()

  # abro el archivo T000gri.LATvec y guardo los datos
  fid = open(metaPath + '/T000gri.LATvec', 'r')
  LATdeg_vec = numpy.fromfile(fid, dtype='float32')
  LATdeg_vec = LATdeg_vec[::-1] # invierto el arreglo porque quedaba invertido verticalmente
  fid.close()

  # abro el archivo T000gri.LONvec y guardo los datos
  fid = open(metaPath + '/T000gri.LONvec', 'r')
  LONdeg_vec = numpy.fromfile(fid, dtype='float32')
  fid.close()

  # obtengo del vector meta el largo y alto de elementos de los vectores y los datos
  Ci = meta[0];
  Cj = meta[1];
  Ct = Ci*Cj;

  print(Ci)
  print(Cj)

  min_lon = point_lon - radius
  max_lon = point_lon + radius
  min_lat = point_lat - radius
  max_lat = point_lat + radius

  # https://stackoverflow.com/questions/10388462/matplotlib-different-size-subplots
  # https://matplotlib.org/tutorials/intermediate/gridspec.html
  gs_kw = dict(width_ratios=[1], height_ratios=[5, 1], hspace=0.05) # width_ratios=[2, 1]
  fig, (a0, a1) = plt.subplots(2, 1, gridspec_kw=gs_kw)

  # genero un mapa con la proyecccion de mercator y lat y lons los anteriores
  ax = Basemap(projection='merc',\
                llcrnrlat=min_lat,urcrnrlat=max_lat,\
                llcrnrlon=min_lon,urcrnrlon=max_lon,\
                resolution='h',\
                ax=a0)

  a1.set_ylim([0, 100])
  a1.set_aspect(aspect=3.164)

  # genero un meshgrid a partir de LonVec y LatVec
  lons2d, lats2d = numpy.meshgrid(LONdeg_vec, LATdeg_vec)
  # y luego obtengo sus coordenadas en el mapa ax
  x, y = ax(lons2d,lats2d)

  vmin        = 0
  vmax        = 100
  ticks       = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
  ticksLabels = ticks

  files = sorted(glob.glob(filesPath+"/*.FR"))
  prod  = getExt(files[0])

  date_ini = getDate(files[0])
  date_fin = getDate(files[-1])

  a1.set_xlim([date_ini, date_fin])

  def animate(i):
    # https://stackoverflow.com/questions/28074461/animating-growing-line-plot-in-python-matplotlib
    # https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time

    fecha = []
    valor = []

    for file in files:

      print(file)

      # abro el archivo file y lo guardo en data
      fid = open(file, 'r')

      if prod == "FR":
        data = numpy.fromfile(fid, dtype='float32')
      elif prod == "CNT":
        data = numpy.fromfile(fid, dtype='int16') # CNT
      else:
        sys.exit("Archivo con extensión incorrecta")

      fid.close()

      # print(numpy.amin(data))
      # print(numpy.amax(data))

      # paso el vector data a una matriz de tamano Ci Cj
      print("len data: " + str(len(data)))
      IMG = numpy.reshape(data, (Ci, Cj))

      # a0.clear()

      # fig.set_figheight(15)
      # fig.set_figwidth(15)

      # dibujo las costas, estados y paises
      ax.drawcoastlines()
      ax.drawstates()
      ax.drawcountries()

      ptx, pty = ax(point_lon, point_lat)
      ax.plot(ptx, pty, 'bo', markersize=2, linewidth=0, color='white', markeredgecolor='none')

      # print('ptx, pty: %f,%f' % (ptx, pty))

      # dibujo los valores de latitudes y longitudes al margen de la imagen, parallels=lat, meridians=lon
      par = ax.drawparallels([point_lat], labels=[1,0,0,0], linewidth=0, fontsize=15, color='white', rotation=90)
      mer = ax.drawmeridians([point_lon], labels=[0,0,1,0], linewidth=0, fontsize=15, color='white')

      setcolor(par,'white')
      setcolor(mer,'white')

      # grafico IMG usando lon como vector x y lat como vector y
      cs   = ax.pcolormesh(x, y, IMG, cmap='jet', vmin=vmin, vmax=vmax)
      cbar = ax.colorbar(cs, pad='3%' , ticks=ticks)

      idy = (numpy.abs(LATdeg_vec - point_lat)).argmin()
      # print(idy)

      idx = (numpy.abs(LONdeg_vec - point_lon)).argmin()
      # print(idx)

      # print(IMG[idy][idx])

      date = getDate(file)
      print(valor)
      fecha.append(date)
      valor.append(IMG[idy][idx])

      # a1.clear()
      a1.plot(fecha, valor, '.-')
      a1.set_xlim([date_ini, date_fin])

      # if prod == "FR":
      #   cbar.ax.set_xlabel("Factor de reflectancia (%)", fontsize=10, color='white')
      #   cbar.ax.set_xticklabels(ticksLabels, fontsize=10, color='white')
      # else:
      #   cbar.ax.set_xlabel("Número de elementos por grilla", fontsize=10, color='white')
      #   cbar.ax.set_xticklabels(ticksLabels, fontsize=10, color='white')

      # print("show")

      # plt.savefig(file + '_img.png', bbox_inches='tight', transparent=True) #

      # fig.canvas.draw()
      # plt.show(block=False)
      # plt.show()  # display it

      # try:
      #   input("Press enter to continue...")
      # except SyntaxError:
      #   print("Closing figure")
      #   pass

      # time.sleep(1)
    # end for files

  ani = animation.FuncAnimation(fig, animate, interval=2000)
  plt.show()

# fileToPng

PATHfile = '/home/chrono/Escritorio/graficas/plotfr/files/'
base     = '/home/chrono/Escritorio/graficas/plotfr/'
meta     = base + 'meta015/'

coordenada_lat   = -31.272756
coordenada_lon   = -57.89092
coordenada_radio = 0.25

fileToPng(PATHfile, meta, coordenada_lat, coordenada_lon, coordenada_radio)
