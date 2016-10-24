  # -*- coding: utf-8 -*-

import matplotlib as _mpl
import matplotlib.colors as _mplc
import math

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

def getColorRange(tMin, tMax):

  # hyaku es el 100% de la franja de temperatura que quiero representar
  hyaku = abs(tMax - tMin)

  # encuentro a que porcentaje se correspone el rango de temperaturas negativas de la escala
  porcentajeColor = (-30 - tMin) * 100. / hyaku

  # determino a cuantos pixeles se corresponde la franja de color de los 1024
  pixelesColor = porcentajeColor * 1024. / 100.

  # determino la cantidad de pixeles de cada color discreto
  pixelesPorFranja = int(pixelesColor / 10.)

  # determino la cantidad de pixeles correspondientes a la escala de grises
  pixelesGris = 1024 - (pixelesPorFranja * 10)

  color_arr = []
  
  franjaMin = 1
  franjaMax = pixelesPorFranja
  iT  = 1024
  
  for valor in range(franjaMin,franjaMax):
    color_arr.append([55/255., 0, 0])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([153/255., 0, 0])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([153/255., 0, 153/255.])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([255/255., 0, 0])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([255/255., 102/255., 0])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([255/255., 255/255., 0])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([0, 153/255., 0])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([0, 255/255., 0])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([0, 0, 255/255.])

  franjaMin = franjaMax
  franjaMax += pixelesPorFranja

  for valor in range(franjaMin,franjaMax):
    color_arr.append([0, 153/255., 153/255.])
  
  # El color inicial de la escala de grises
  colorGris = 0.85
  step      = colorGris / pixelesGris
  
  color_arr.append([colorGris, colorGris, colorGris])
  
  # de gris a negro
  for valor in range(franjaMax, 1024-1):
    colorGris -= step
    color_arr.append([colorGris, colorGris, colorGris])
  
  color_arr.append([0, 0, 0])
  
  return color_arr
  
# def getColorRange()

#########################################
#########################################
#########################################

def getInumetColorRange():
  color_arr = []
  
  i01 = 40
  i02 = 80
  i03 = 118
  i04 = 158
  i05 = 197
  i06 = 236
  i07 = 276
  i08 = 316
  i09 = 354
  i10 = 394
  iT  = 1024
  
  for valor in range(1,i01):
    color_arr.append([55/255., 0, 0])
  for valor in range(i01, i02):
    color_arr.append([153/255., 0, 0])
  for valor in range(i02, i03):
    color_arr.append([153/255., 0, 153/255.])
  for valor in range(i03, i04):
    color_arr.append([255/255., 0, 0])
  for valor in range(i04, i05):
    color_arr.append([255/255., 102/255., 0])
  for valor in range(i05, i06):
    color_arr.append([255/255., 255/255., 0])
  for valor in range(i06, i07):
    color_arr.append([0, 153/255., 0])
  for valor in range(i07, i08):
    color_arr.append([0, 255/255., 0])
  for valor in range(i08, i09):
    color_arr.append([0, 0, 255/255.])
  for valor in range(i09, i10):
    color_arr.append([0, 153/255., 153/255.])
  
  # 630 intervalos
  base = 0.85
  step = base / (iT - i10)
  
  color_arr.append([base, base, base])
  
  # de gris a negro
  for valor in range(i10, iT-1):
    base -= step
    color_arr.append([base, base, base])
  
  color_arr.append([0, 0, 0])
  
  return color_arr
  
# def getInumetColorRange()

#########################################
#########################################
#########################################

# Inumet v2 color range

def getInumetV2CR():
  color_arr = []
  
  i01 = 77
  i02 = 154
  i03 = 231
  i04 = 308
  i05 = 385
  i06 = 462
  i07 = 539
  i08 = 616
  i09 = 693
  i10 = 770
  iT  = 1024
  
  for valor in range(1,i01):
    color_arr.append([55/255., 0, 0])
  for valor in range(i01, i02):
    color_arr.append([153/255., 0, 0])
  for valor in range(i02, i03):
    color_arr.append([153/255., 0, 153/255.])
  for valor in range(i03, i04):
    color_arr.append([255/255., 0, 0])
  for valor in range(i04, i05):
    color_arr.append([255/255., 102/255., 0])
  for valor in range(i05, i06):
    color_arr.append([255/255., 255/255., 0])
  for valor in range(i06, i07):
    color_arr.append([0, 153/255., 0])
  for valor in range(i07, i08):
    color_arr.append([0, 255/255., 0])
  for valor in range(i08, i09):
    color_arr.append([0, 0, 255/255.])
  for valor in range(i09, i10):
    color_arr.append([0, 153/255., 153/255.])
  
  # 630 intervalos
  base = 0.85
  step = base / (iT - i10)
  
  color_arr.append([base, base, base])
  
  # de gris a negro
  for valor in range(i10, iT-1):
    base -= step
    color_arr.append([base, base, base])
  
  color_arr.append([0, 0, 0])
  
  return color_arr
  
# def getInumetV2CR()

#########################################
#########################################
#########################################

# Inumet v3 color range

def getInumetV3():
  color_arr = []
  
  i01 = 40
  i02 = 80
  i03 = 120
  i04 = 160
  i05 = 200
  i06 = 240
  i07 = 280
  i08 = 320
  i09 = 360
  i10 = 400
  iT  = 1024
  
  for valor in range(1,i01):
    color_arr.append([55/255., 0, 0])
  for valor in range(i01, i02):
    color_arr.append([153/255., 0, 0])
  for valor in range(i02, i03):
    color_arr.append([153/255., 0, 153/255.])
  for valor in range(i03, i04):
    color_arr.append([255/255., 0, 0])
  for valor in range(i04, i05):
    color_arr.append([255/255., 102/255., 0])
  for valor in range(i05, i06):
    color_arr.append([255/255., 255/255., 0])
  for valor in range(i06, i07):
    color_arr.append([0, 153/255., 0])
  for valor in range(i07, i08):
    color_arr.append([0, 255/255., 0])
  for valor in range(i08, i09):
    color_arr.append([0, 0, 255/255.])
  for valor in range(i09, i10):
    color_arr.append([0, 153/255., 153/255.])
  
  base = 0.85
  step = base / (iT - i10)
  
  color_arr.append([base, base, base])
  
  # de gris a negro
  for valor in range(i10, iT-1):
    base -= step
    color_arr.append([base, base, base])
  
  color_arr.append([0, 0, 0])
  
  return color_arr
  
# def getInumetV3()

#########################################
#########################################
#########################################

def colorArray(N, tMin, tMax):

  # col_seq = getInumetColorRange()
  col_seq = getColorRange(tMin, tMax)
  # col_seq = getInumetV3()

  seqLen  = len(col_seq)
  delta   = 1.0/(seqLen - 1)
  r_tuple = ((i*delta, col_seq[i][0], col_seq[i][0]) for i in range(seqLen))
  g_tuple = ((i*delta, col_seq[i][1], col_seq[i][1]) for i in range(seqLen))
  b_tuple = ((i*delta, col_seq[i][2], col_seq[i][2]) for i in range(seqLen))
  cdict   = {'red':   tuple(r_tuple),
             'green': tuple(g_tuple),
             'blue':  tuple(b_tuple)}
  cwm = _mpl.colors.LinearSegmentedColormap('Inumet', cdict, N)
  return cwm

# def colorArray(N)
