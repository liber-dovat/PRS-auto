#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import struct
import numpy

from mpl_toolkits.basemap import Basemap

# http://scipy-cookbook.readthedocs.io/items/Matplotlib_Loading_a_colormap_dynamically.html
def gmtColormap(fileName,GMTPath = None,segmentos = 1024):
      import colorsys
      import numpy
      N = numpy
      if type(GMTPath) == type(None):
          filePath = "/usr/local/cmaps/"+ fileName+".cpt"
      else:
          filePath = GMTPath+"/"+ fileName +".cpt"
      try:
          f = open(filePath)
      except:
          print "file ",filePath, "not found"
          return None

      lines = f.readlines()
      f.close()

      x = []
      r = []
      g = []
      b = []
      colorModel = "RGB"
      for l in lines:
          ls = l.split()
          if l[0] == "#":
             if ls[-1] == "HSV":
                 colorModel = "HSV"
                 continue
             else:
                 continue
          if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
             pass
          else:
              x.append(float(ls[0]))
              r.append(float(ls[1]))
              g.append(float(ls[2]))
              b.append(float(ls[3]))
              xtemp = float(ls[4])
              rtemp = float(ls[5])
              gtemp = float(ls[6])
              btemp = float(ls[7])

      x.append(xtemp)
      r.append(rtemp)
      g.append(gtemp)
      b.append(btemp)

      nTable = len(r)
      x = N.array( x , N.float)
      r = N.array( r , N.float)
      g = N.array( g , N.float)
      b = N.array( b , N.float)
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "RGB":
          r = r/255.
          g = g/255.
          b = b/255.
      xNorm = (x - x[0])/(x[-1] - x[0])

      red = []
      blue = []
      green = []
      for i in range(len(x)):
          red.append([xNorm[i],r[i],r[i]])
          green.append([xNorm[i],g[i],g[i]])
          blue.append([xNorm[i],b[i],b[i]])
      colorDict = {"red":red, "green":green, "blue":blue}
      cwm = matplotlib.colors.LinearSegmentedColormap(fileName, colorDict, segmentos)
      return cwm

# gmtColormap

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

def uruMap(outPngPathAndName):

  min_lon = -58.6
  max_lon = -52.9
  min_lat = -35.
  max_lat = -30.

  # print "Lon min:" + str(min_lon) + ", Lon max:" + str(max_lon)
  # print "Lat min:" + str(min_lat) + ", Lat max:" + str(max_lat)

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  axes = plt.gca()
  axes.set_xlim([min_lon, max_lon])
  axes.set_ylim([min_lat, max_lat])

  # genero un mapa con la proyecccion de mercator y lat y lons los anteriores
  ax = Basemap(projection='merc',\
                llcrnrlat=min_lat,urcrnrlat=max_lat,\
                llcrnrlon=min_lon,urcrnrlon=max_lon,\
                epsg=4269,\
                resolution='h')

  # dibujo las costas, estados y paises
  ax.drawcoastlines()
  ax.drawstates()
  ax.drawcountries()
  # ax.shadedrelief()
  # ax.etopo()
  ax.arcgisimage(service='World_Physical_Map', xpixels = 2000, verbose= True)

  # dibujo los valores de latitudes y longitudes al margen de la imagen
  # par = ax.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10, color='white')
  # mer = ax.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10, color='white')

  setcolor(par,'white')
  setcolor(mer,'white')

  # guardo la imagen en la ruta destino
  plt.savefig(outPngPathAndName, bbox_inches='tight', dpi=200, transparent=True)
  plt.close() # cierro el archivo

# fileToPng

path = "/home/ldovat/dev/PRS-sat/PRSpost/test/mapa/mapaUruguay.png"

uruMap(path)
