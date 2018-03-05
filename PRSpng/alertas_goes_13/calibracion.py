import numpy

# http://stackoverflow.com/questions/11442191/parallelizing-a-numpy-vector-operation
# leer para paralelizar
# http://www.star.nesdis.noaa.gov/smcd/spb/fwu/homepage/GOES_Imager_Vis_OpCal_G13.php
# Correccion de muestras

# Rpre  = (dato - b)/m
# C = alfa * exp(beta * dt)
# Rpost = Rpre * C

def Radiance(dato,m,b):
  return (dato - b)/m
# Radiance

#########################################
#########################################
#########################################

def temperaturaReal(dato,m,b1,n,a,b2):
  c1 = 0.000011911
  c2 = 1.438833

  lx   = (dato/32.0 - b1) / m
  aux  = 1 + ( (c1*numpy.power(n, 3)) / lx )
  Teff = (c2*n) / numpy.log(aux)
  Temp = a + b2 * Teff

  return Temp - 273.0
# temperaturaReal

#########################################
#########################################
#########################################

def calibrarData(banda, data):

  # seteo las variables en funcion de las bandas
  if banda == 1:
    m = 227.3889
    b = 68.2167
  elif banda == 2:
    m  = 227.3889
    b1 = 68.2167
    n  = 2561.74
    a  = -1.437204
    b2 = 1.002562
  elif banda == 3:
    m  = 38.8383
    b1 = 29.1287
    n  = 1522.52
    a  = -3.625663
    b2 = 1.010018
  elif banda == 4:
    m  = 5.2285
    b1 = 15.6854
    n  = 937.23
    a  = -0.386043
    b2 = 1.001298
  elif banda == 6:
    m  = 5.5297
    b1 = 16.5892
    n  = 749.83
    a  = -0.134801
    b2 = 1.000482

  # aplico la funcion como un map en cada elemento
  if banda == 1:
    return Radiance(data,m,b)
  else:
    vfunc = numpy.vectorize(temperaturaReal)
    return vfunc(data,m,b1,n,a,b2)

# calibrarData
