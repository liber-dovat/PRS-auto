#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import struct
import numpy
import os

from os.path              import basename

# RUTAsat = '/sat/prd-sat/ART_G015x015GG_C015x015/'
# PATHfr  = RUTAsat + 'B01-FR/2016/ART_2016275_143500.FR'

# print PATHfr

def frtopng(metaPath, file):

  fid = open(metaPath + '/T000gri.META', 'r')
  meta = numpy.fromfile(fid, dtype='float32')
  fid.close()

  fid = open(metaPath + '/T000gri.LATvec', 'r')
  LATdeg_vec = numpy.fromfile(fid, dtype='float32')
  LATdeg_vec = LATdeg_vec[::-1] # invierto el arreglo porque quedaba invertido verticalmente
  fid.close()

  fid = open(metaPath + '/T000gri.LONvec', 'r')
  LONdeg_vec = numpy.fromfile(fid, dtype='float32')
  fid.close()

  # obtengo del vector meta el largo y alto de elementos de los vectores y los datos
  Ci = meta[0];
  Cj = meta[1];
  Ct = Ci*Cj;

  print "Lon min:" + str(numpy.amin(LONdeg_vec)) + ", Lon max:" + str(numpy.amax(LONdeg_vec))
  print "Lat min:" + str(numpy.amin(LATdeg_vec)) + ", Lat max:" + str(numpy.amax(LATdeg_vec))

  # plt.axis('scaled')

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  axes = plt.gca()
  axes.set_xlim([numpy.amin(LONdeg_vec),numpy.amax(LONdeg_vec)])
  axes.set_ylim([numpy.amin(LATdeg_vec),numpy.amax(LATdeg_vec)])

  # abro el archivo FR
  fid = open(file, 'r')
  data = numpy.fromfile(fid, dtype='float32')
  fid.close()
  IMG1 = numpy.reshape(data, (Ci, Cj))
  print IMG1.shape

  # grafico IMG1 usando lon como vector x y lat como vector y
  cs = plt.pcolormesh(LONdeg_vec, LATdeg_vec, IMG1, cmap='jet')

  # dado que FR y RP van de 0 a 100 seteo esos rangos para el colorbar
  plt.clim(0,100)

  # agrego el colorbar
  cbar = plt.colorbar(cs, ticks=[0., 20., 40., 60., 80., 100.])
  cbar.ax.set_xticklabels([0., 20., 40., 60., 80., 100.], fontsize=10)

  # agrego el logo en el documento
  logo = plt.imread('/sat/PRS/libs/PRS-auto/PRSpng/imgs/les-logo.png')
  plt.figimage(logo, 5, 5)

  name = basename(file)

  # genero el pie de la imagen, con el logo y la info del arcivo
  plt.annotate(name, (0,0), (140, -25), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=12, family='monospace')

  PATHpng = './test_fr/png/'
  plt.savefig(PATHpng + name +'.png', bbox_inches='tight', dpi=200)
  plt.close() # cierro el archivo

# frtopng

frtopng('./test_fr/meta/', './test_fr/B01-FR/2016/ART_2016285_133500.FR')
frtopng('./test_fr/meta/', './test_fr/B01-RP/2016/ART_2016285_133500.RP')
