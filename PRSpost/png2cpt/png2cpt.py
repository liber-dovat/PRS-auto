#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from os.path import basename
from PIL     import Image

# Éste script recibe como parámetro un archivo png con el dibujo del
# colormap deseado. El colormap tiene tantas líneas como ancho tiene
# la imagen. Por cada columna del archivo png se agrega una línea
# al colormap. Las columnas tienen que ser cada una con un color
# uniforme.
# Se recomienda utilizar inkscape para generar el png, y exportarlo 
# a una imagen de largo 1024 aprox, según el ancho del colormap que
# se desea generar.

if len(sys.argv) < 2:
  print "Falta como parámetro el nombre del archivo .png a procesar"
else:
  filename = basename(sys.argv[1])
  im = Image.open(filename, 'r')
  width, height = im.size
  pixel_values = list(im.getdata())

  # print pixel_values

  # print len(pixel_values)

  print "# " + filename
  print "# Generado utilizando png2cpt.py"
  print "# https://github.com/liber-dovat"
  print "# COLOR_MODEL = RGB"

  for i in range(1, width):

    print str(i)\
      + " " + str(pixel_values[i-1][0])\
      + " " + str(pixel_values[i-1][1])\
      + " " + str(pixel_values[i-1][2])\
      + " " + str(i+1)\
      + " " + str(pixel_values[i][0])\
      + " " + str(pixel_values[i][1])\
      + " " + str(pixel_values[i][2])

  print "N 128 128 128"
