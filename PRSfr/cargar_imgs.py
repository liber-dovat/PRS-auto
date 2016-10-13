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

  numpy.set_printoptions(suppress=True)
  # print meta
  # print Ci
  # print Cj
  # print Ct
  # print LATdeg_vec.size
  # print LATdeg_vec.size

  print "Lon min:" + str(numpy.amin(LONdeg_vec)) + ", Lon max:" + str(numpy.amax(LONdeg_vec))
  print "Lat min:" + str(numpy.amin(LATdeg_vec)) + ", Lat max:" + str(numpy.amax(LATdeg_vec))

  # plt.axis('scaled')

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  axes = plt.gca()
  axes.set_xlim([numpy.amin(LONdeg_vec),numpy.amax(LONdeg_vec)])
  axes.set_ylim([numpy.amin(LATdeg_vec),numpy.amax(LATdeg_vec)])

  name = basename(file)
  extencion = name.split('.')[-1]
  # print extencion

  # Si FR|RP|T2|T3|T4|T6 dtype es float32
  # MK o C1 es int16
  # abro el archivo FR
  if extencion == 'MK' or extencion == 'C1':
    dtype = 'int16'
  else:
    dtype = 'float32'

  # abro el archivo pasado por parametro
  fid = open(file, 'r')
  data = numpy.fromfile(fid, dtype=dtype)
  fid.close()
  # print data.size
  IMG = numpy.reshape(data, (Ci, Cj))
  # print IMG.shape

  # grafico IMG1 usando lon como vector x y lat como vector y
  cs = plt.pcolormesh(LONdeg_vec, LATdeg_vec, IMG, cmap='jet')

  # dado que FR y RP van de 0 a 100 seteo esos rangos para el colorbar
  if extencion == 'MK' or extencion == 'C1':
    cbar = plt.colorbar(cs)
    print IMG
  else:
    plt.clim(0,100)
    # agrego el colorbar
    cbar = plt.colorbar(cs, ticks=[0., 20., 40., 60., 80., 100.])
    cbar.ax.set_xticklabels([0., 20., 40., 60., 80., 100.], fontsize=10)

  # agrego el logo en el documento
  logo = plt.imread('/sat/PRS/libs/PRS-auto/PRSpng/imgs/les-logo.png')
  plt.figimage(logo, 5, 5)

  # genero el pie de la imagen, con el logo y la info del arcivo
  plt.annotate(name, (0,0), (140, -25), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=12, family='monospace')

  PATHpng = './test_fr/png/'
  plt.savefig(PATHpng + name +'.png', bbox_inches='tight', dpi=200)
  plt.close() # cierro el archivo

# frtopng

# frtopng('./test_fr/meta15/', './test_fr/imgs/ART_2016285_133500.FR')
# frtopng('./test_fr/meta15/', './test_fr/imgs/ART_2016285_133500.RP')
frtopng('./test_fr/meta15/', './test_fr/imgs/MKART_2016285_133500.MK')
# frtopng('./test_fr/meta60/', './test_fr/imgs/B02ART_2016285_133500.MK')