#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy
import math
import glob
import calendar
from datetime import date, datetime
from loc_types import *

def getCsvLocs(file):

  name = numpy.genfromtxt(file, delimiter=' ', dtype=None, unpack=True, skip_header=3, usecols=(1,2,3))

  locs_dic_coord = dict()

  for val in name:
    key = str(val[0])[2:5]
    locs_dic_coord[key] = [float(val[1]), float(val[2])]

  return locs_dic_coord

# getCsvCols

def doy(Y,M,D):
  """ given year, month, day return day of year
      Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """
  if calendar.isleap(Y):
      K = 1
  else:
      K = 2
  N = int((275 * M) / 9.0) - K * int((M + 9) / 12.0) + D - 30
  return N

# doy

def cantDias(Y):
  if calendar.isleap(Y):
    return 366
  else:
    return 365
# cantDias

def declinacionSolar(gamma):
  DELTArad = 0.006918 - 0.399912*math.cos(gamma) + 0.070257*math.sin(gamma) - 0.006758*math.cos(2*gamma) + 0.000907*math.sin(2*gamma) - 0.002697*math.cos(3*gamma) + 0.00148*math.sin(3*gamma);
  return float(DELTArad)
# declinacionSolar

# calculo ecuacion horaria (Es 0.000075, hay una errata en el coso de Gonzalo)
def ecuacionHoraria(gamma):
  c = 229.18;  # cte en min para la aprox de la ecuacion de tiempo 
  EcTmin = c*(0.000075 + 0.001868*math.cos(gamma) - 0.032077*math.sin(gamma) - 0.014615*math.cos(2*gamma) - 0.04089*math.sin(2*gamma));
  return float(EcTmin)
# ecuacionHoraria

# retorna el calculo del coseno del angulo zenital para la ubicacion, hora y fecha pasadas por parametro
# https://www.esrl.noaa.gov/gmd/grad/solcalc/azel.html
# AZ -34.918224, -56.16653
# 34°55'05.6"S 56°09'59.5"W
def cosSolarZenithAngle(phi, psi, datetime):
  # phi = lat <ubicacion>
  # psi = lon <ubicacion>
  # theta_s = solar zenith angle
  # delta = declination of the Sun
  # hora_solar
  # hora_local, con fraccion
  # omega = hour angle, in the local solar time.
  # cos(theta_s)= sen(phi)*sen(delta) + cos(phi)cos(delta)cos(omega)

  phi = math.radians(phi) # convierto phi a radianes
  pi  = math.pi

  Y = datetime.year
  M = datetime.month
  D = datetime.day
  h = float(datetime.hour)
  m = datetime.minute/60.0
  hora_local = h + m

  today_doy  = float(doy(Y,M,D))
  cant_dias  = float(cantDias(Y))
  gamma      = (2.0*pi*(today_doy-1.0))/cant_dias # calculo de gamma
  delta      = declinacionSolar(gamma)
  E          = ecuacionHoraria(gamma)
  hora_solar = hora_local + (psi+45.0)/15.0 + E/60.0 # psi en grados
  omega      = ((hora_solar-12.0)*pi)/12.0

  # print "Doy:%f, Dias:%f %f:%f %f gamma:%f delta:%f E:%f hora_solar:%f omega:%f" % (today_doy, cant_dias, h,m, hora_local, gamma, delta, E, hora_solar, omega)

  cz = math.sin(phi)*math.sin(delta) + math.cos(phi)*math.cos(delta)*math.cos(omega)
  if cz < 0:
    cz = 0

  return cz

# solarZenithAngle

def locValueArray2Array(locValueArray):

  new_array_mean = []
  new_array_msk  = []
  new_array_cnt  = []

  for item in locValueArray:
    new_array_mean.append(item.valor)
    new_array_msk.append(item.msk)
    new_array_cnt.append(item.cnt)

  return new_array_mean, new_array_msk, new_array_cnt
# locValueArray2Array

def locDateArray2Array(locDateArray):

  new_array_date = []

  for item in locDateArray:
    new_array_date.append(float(item.year))
    new_array_date.append(float(item.doy))
    new_array_date.append(float(item.hh))
    new_array_date.append(float(item.mm))
    new_array_date.append(float(item.ss))
    new_array_date.append(float(item.ite))

  return new_array_date
# locDateArray2Array

def getJILess(loc_lat, loc_lon, loc_res, LATdeg_vec, LONdeg_vec):

  min_lon = loc_lon - float(loc_res)
  max_lon = loc_lon + float(loc_res)
  min_lat = loc_lat - float(loc_res)
  max_lat = loc_lat + float(loc_res)

  # print("min_lon: %f"%(min_lon))
  # print("max_lon: %f"%(max_lon))
  # print("min_lat: %f"%(min_lat))
  # print("max_lat: %f"%(max_lat))

  # genero un meshgrid a partir de LonVec y LatVec
  lons2d, lats2d = numpy.meshgrid(LONdeg_vec, LATdeg_vec)

  j_less  = len(lons2d)
  j_great = 0

  i_less  = len(lats2d)
  i_great = 0

  for i in range(0,len(lons2d)):      # recorro verticalmente
    for j in range(0,len(lons2d[0])): # recorro horizontalmente
      if (lons2d[i][j] > min_lon) and\
         (lons2d[i][j] < max_lon) and\
         (lats2d[i][j] > min_lat) and\
         (lats2d[i][j] < max_lat):
        if j < j_less:
          j_less = j
        if j > j_great:
          j_great = j

        if i < i_less:
          i_less = i
        if i > i_great:
          i_great = i

  # print('x,%d,%d y,%d,%d' % (j_less, j_great, i_less, i_great))
  return j_less, j_great, i_less, i_great

# getJILess

def getIJArray(loc_lat, loc_lon, spatial_lat, spatial_lon, LATdeg_vec, LONdeg_vec):

  min_lat = loc_lat - float(spatial_lat/2.0)
  max_lat = loc_lat + float(spatial_lat/2.0)
  min_lon = loc_lon - float(spatial_lon/2.0)
  max_lon = loc_lon + float(spatial_lon/2.0)

  coord_i = []
  coord_j = []

  # print("min_lon: %f"%(min_lon))
  # print("max_lon: %f"%(max_lon))
  # print("min_lat: %f"%(min_lat))
  # print("max_lat: %f"%(max_lat))

  # genero un meshgrid a partir de LonVec y LatVec
  lons2d, lats2d = numpy.meshgrid(LONdeg_vec, LATdeg_vec)

  for i in range(0,len(lons2d)):      # recorro verticalmente
    for j in range(0,len(lons2d[0])): # recorro horizontalmente
      if (lons2d[i][j] > min_lon) and\
         (lons2d[i][j] < max_lon) and\
         (lats2d[i][j] > min_lat) and\
         (lats2d[i][j] < max_lat):     # si estoy dentro de la ventana
        coord_i.append(i)
        coord_j.append(j)

  # print('x,%d,%d y,%d,%d' % (j_less, j_great, i_less, i_great))
  return coord_i, coord_j

# getJIArray

def getJILessShared(locs_dic_coord, parametros):

  key        = parametros[0]
  loc_lat    = parametros[1]
  loc_lon    = parametros[2]
  loc_res    = parametros[3]
  LATdeg_vec = parametros[4]
  LONdeg_vec = parametros[5]

    # p = Process(target=getJILessShared, args=(locs_dic_coord, parametros))

  min_lon = loc_lon - float(loc_res)
  max_lon = loc_lon + float(loc_res)
  min_lat = loc_lat - float(loc_res)
  max_lat = loc_lat + float(loc_res)

  # print("min_lon: %f"%(min_lon))
  # print("max_lon: %f"%(max_lon))
  # print("min_lat: %f"%(min_lat))
  # print("max_lat: %f"%(max_lat))

  # genero un meshgrid a partir de LonVec y LatVec
  lons2d, lats2d = numpy.meshgrid(LONdeg_vec, LATdeg_vec)

  j_less  = len(lons2d)
  j_great = 0

  i_less  = len(lats2d)
  i_great = 0

  for i in range(0,len(lons2d)):      # recorro verticalmente
    for j in range(0,len(lons2d[0])): # recorro horizontalmente
      if (lons2d[i][j] > min_lon) and\
         (lons2d[i][j] < max_lon) and\
         (lats2d[i][j] > min_lat) and\
         (lats2d[i][j] < max_lat):
        if j < j_less:
          j_less = j
        if j > j_great:
          j_great = j

        if i < i_less:
          i_less = i
        if i > i_great:
          i_great = i

  # print('x,%d,%d y,%d,%d' % (j_less, j_great, i_less, i_great))
  # return j_less, j_great, i_less, i_great

  print("Clave: %s"%key)

  locs_dic_coord[key] = [loc_lat, loc_lon, j_less, j_great, i_less, i_great]
  # locs_dic_coord[key].append([loc_lat, loc_lon, j_less, j_great, i_less, i_great])
# getJILess