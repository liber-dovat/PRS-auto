#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import numpy
import math
import glob
import calendar
from datetime import date, datetime
# from pysolar.solar import * # sudo apt-get install python-pysolr python-pysolar # https://stackoverflow.com/questions/45238223/how-to-get-solar-zenith-angle-using-pysolar
# from pysolar import solar
# https://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python

def getCsvCols(path):
  tabla_valores = [float('nan')]*144
  tabla_count   = [0]*144

  for file in sorted(glob.iglob(path)):
    text = numpy.genfromtxt(file, delimiter=',' , names=True, dtype=None)

    try:
      dato = float(str(text['GHI1_AV_Wm2']))
    except ValueError:
      dato = float('nan')

    timestamp = str(text['Timestamp'])
    # la formula para mapear el indice es hora*6+floor(min/10)
    big_index   = int(timestamp[11:13])*6 # obtengo la hora * 6
    small_index = int(timestamp[14:16])//10
    tabla_index = big_index + small_index

    # print timestamp
    # print dato
    # print big_index
    # print small_index
    # print tabla_index

    tabla_valores[tabla_index] = numpy.nansum([tabla_valores[tabla_index], dato])
    tabla_count[tabla_index]   += 1

    # print tabla_valores[tabla_index]
    # print tabla_count[tabla_index]

  # for file

  for i in range(0,143):
    if tabla_count[i] != 0:
      tabla_valores[i] /= tabla_count[i]

  return tabla_valores

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

# path = 'datos_AZ/*.csv'
# path = 'datos_AZ/AZ_DT_20181203T181900.csv'
# tabla_valores = getCsvCols(path)

# for i in tabla_valores:
#   print i 

# dia = datetime.now()
# print dia.year
# print dia.month
# print dia.day
# print dia.hour
# print dia.minute
# AZ_lat = -34.918224
# AZ_lon = -56.16653

# cz = cosSolarZenithAngle(-34.918224, -56.16653, dia)
# print cz

# dobj = datetime.datetime(2018,12,7,7,tzinfo=datetime.timezone.utc) - datetime.timedelta(hours=-3)
# sza = float(90) - solar.get_altitude(-34.918224, -56.16653, dobj)
# print ("timezone = UTC-4,",sza)
