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
def tempToValue(temp, band):

  # i01 = 60
  # i02 = 120
  # i03 = 180
  # i04 = 240
  # i05 = 300
  # i06 = 360
  # i07 = 420
  # i08 = 480
  # i09 = 540
  # i10 = 600
  # iT  = 1024

  # el rango de temperaturas depende de la banda
  i01 = -75.
  i02 = -70.
  i03 = -65.
  i04 = -60.
  i05 = -55.
  i06 = -50.
  i07 = -45.
  i08 = -40.
  i09 = -35.
  i10 = -30.
  iT  = 50.

  # la escala de color se corresponde con el 59.13% del 100%
  # cuando 1024 -> 100%, 59.13 -> 605, aproximando
  px_color = 605
  px_gris  = 419

  middle = px_color/20.
  
  # retorno un valor en el medio de la franja para no caer en un borde
  if temp < -75.:
    return middle
  elif temp in range(i01, i02):
    return 2*middle
  elif temp in range(i02, i03):
    return 3*middle
  elif temp in range(i03, i04):
    return 4*middle
  elif temp in range(i04, i05):
    return 5*middle
  elif temp in range(i05, i06):
    return 6*middle
  elif temp in range(i06, i07):
    return 7*middle
  elif temp in range(i07, i08):
    return 8*middle
  elif temp in range(i08, i09):
    return 9*middle
  elif temp in range(i09, i10):
    return 10*middle
  
  hundred = abs(i10) + iT
  
  return color
