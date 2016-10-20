# -*- coding: utf-8 -*-

'''
-30°C/-34°C -- #009999 -- (0,153,153) -- Celeste
-35°C/-39°C -- #0000FF -- (0,0,255)   -- Azul
-40°C/-44°C -- #00FF00 -- (0,255,0)   -- Verde Claro
-45°C/-49°C -- #009900 -- (0,153,0)   -- Verde
-50°C/-54°C -- #FFFF00 -- (255,255,0) -- Amarillo
-55°C/-59°C -- #FF6600 -- (255,102,0) -- Naranja
-60°C/-64°C -- #FF0000 -- (255,0,0)   -- Rojo
-65°C/-64°C -- #990099 -- (153,0,153) -- Púrpura
-70°C/-69°C -- #990000 -- (153,0,0)   -- Marrón
-75°C/-74°C -- #000000 -- (0,0,0)     -- Negro
'''

'''
elif band == 'T2':
  vmin = -68.
  vmax = 47. 
elif band == 'T3':
  vmin = -68.
  vmax = -8.
elif band == 'T4':
  vmin = -80.
  vmax = 50.
elif band == 'T6':
  vmin = -68.
  vmax = 7.
'''

# dado un valor de temperatura y una banda, mapeo el valor a un entero entre 0 y 1024
def tempToValue(temp, tMin, tMax, middle, pixelesColor, pixelesGris):

  # print "middle: " + str(middle)
  # print "pixelesColor: " + str(pixelesColor)
  # print "pixelesGris: " + str(pixelesGris)

  # el rango de temperaturas es fijo, lo que cambia es el mapeo a color según la banda
  i01 = -75
  i02 = -70
  i03 = -65
  i04 = -60
  i05 = -55
  i06 = -50
  i07 = -45
  i08 = -40
  i09 = -35
  i10 = -30

  # retorno un valor en el medio de la franja para no caer en un borde
  if temp < -75.:
    return middle
  elif temp in range(i01, i02):
    return 3*middle
  elif temp in range(i02, i03):
    return 5*middle
  elif temp in range(i03, i04):
    return 7*middle
  elif temp in range(i04, i05):
    return 9*middle
  elif temp in range(i05, i06):
    return 11*middle
  elif temp in range(i06, i07):
    return 13*middle
  elif temp in range(i07, i08):
    return 15*middle
  elif temp in range(i08, i09):
    return 17*middle
  elif temp in range(i09, i10):
    return 19*middle
  elif temp >= i10:

    offsetPixelGris = (temp * pixelesGris) / tMax

    return pixelesColor + offsetPixelGris
  else:
    return 512

# tempToValue

#########################################
#########################################
#########################################

# dado un valor de temperatura y una banda, mapeo el valor a un entero entre 0 y 1024
def tempToValueV2(temp, tMin, tMax, middle, pixelesColor, pixelesGris):

  # el rango de temperaturas es fijo, lo que cambia es el mapeo a color según la banda
  i01 = -75
  i02 = -70
  i03 = -65
  i04 = -60
  i05 = -55
  i06 = -50
  i07 = -45
  i08 = -40
  i09 = -35
  i10 = -30

  # retorno un valor en el medio de la franja para no caer en un borde
  if temp < -75.:
    return middle
  elif temp in range(i01, i02):
    return 3*middle
  elif temp in range(i02, i03):
    return 5*middle
  elif temp in range(i03, i04):
    return 7*middle
  elif temp in range(i04, i05):
    return 9*middle
  elif temp in range(i05, i06):
    return 11*middle
  elif temp in range(i06, i07):
    return 13*middle
  elif temp in range(i07, i08):
    return 15*middle
  elif temp in range(i08, i09):
    return 17*middle
  elif temp in range(i09, i10):
    return 19*middle
  else:

    offsetPixelGris = (temp * pixelesGris) / tMax

    return pixelesColor + offsetPixelGris

# tempToValueV2

#########################################
#########################################
#########################################

# dado un valor de temperatura y una banda, mapeo el valor a un entero entre 0 y 1024
def tempToValueV3(temp, tMin, tMax, middle, pixelesColor, pixelesGris):

  # el rango de temperaturas es fijo, lo que cambia es el mapeo a color según la banda
  i01 = -75
  i02 = -70
  i03 = -65
  i04 = -60
  i05 = -55
  i06 = -50
  i07 = -45
  i08 = -40
  i09 = -35
  i10 = -30

  # retorno un valor en el medio de la franja para no caer en un borde
  if temp < -75.:
    return middle
  elif temp in range(i01, i02):
    return 3*middle
  elif temp in range(i02, i03):
    return 5*middle
  elif temp in range(i03, i04):
    return 7*middle
  elif temp in range(i04, i05):
    return 9*middle
  elif temp in range(i05, i06):
    return 11*middle
  elif temp in range(i06, i07):
    return 13*middle
  elif temp in range(i07, i08):
    return 15*middle
  elif temp in range(i08, i09):
    return 17*middle
  elif temp in range(i09, i10):
    return 19*middle
  else:

    offsetPixelGris = (temp * pixelesGris) / tMax

    return pixelesColor + offsetPixelGris

# tempToValueV3

#########################################
#########################################
#########################################

def pixelesFranja(tMin, tMax):

  if tMax < 0:
    pixelesColor = 1024
    pixelesGris  = 0
    middle       = 102.4
  else:

    # hyaku es el 100% de la franja de temperatura que quiero representar
    hyaku = abs(tMax - tMin)

    # encuentro a que porcentaje se correspone el rango de temperaturas negativas de la escala
    porcentajeColor = abs(tMin) * 100. / hyaku

    # determino a cuantos pixeles se corresponde la franja de color de los 1024
    pixelesColor = porcentajeColor * 1024. / 100.

    # determino la cantidad de pixeles de cada color discreto
    pixelesPorFranja = int(pixelesColor / 10.)

    # determino la cantidad de pixeles correspondientes a la escala de grises
    pixelesGris = 1024 - (pixelesPorFranja * 10)

    middle = pixelesPorFranja / 2

  # if

  return middle, pixelesColor, pixelesGris

# pixelesFranja

#########################################
#########################################
#########################################

def pixelesFranjaV2(tMin, tMax):

  middle       = 38.5
  pixelesColor = 770
  pixelesGris  = 254

  return middle, pixelesColor, pixelesGris

# pixelesFranjaV2

#########################################
#########################################
#########################################

def pixelesFranjaV3(tMin, tMax):

  middle       = 20
  pixelesColor = 400
  pixelesGris  = 624

  return middle, pixelesColor, pixelesGris

# pixelesFranjaV3