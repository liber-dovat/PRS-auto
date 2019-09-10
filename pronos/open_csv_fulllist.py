#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import numpy
import glob

def getCsvCols(path):
  tabla_tiempo = []
  tabla_dato   = []
  for file in sorted(glob.iglob(path)):
    text = numpy.genfromtxt(file, delimiter=',' , names=True, dtype=None)
    tabla_tiempo.append(text['Timestamp'])
    tabla_dato  .append(text['GHI1_AV_Wm2'])

  # print len(tabla_tiempo)
  # print len(tabla_dato)
  # for i in range(len(tabla_tiempo)):
  #   print "%s %f" % (tabla_tiempo[i], tabla_dato[i])

  return tabla_tiempo, tabla_dato

path = 'datos_AZ/*.csv'
tabla_tiempo, tabla_dato = getCsvCols(path)

# for i in tabla_tiempo:
#   print i 
