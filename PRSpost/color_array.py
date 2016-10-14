import matplotlib as _mpl
import matplotlib.colors as _mplc

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
    color_arr.append([0, 0, 0])
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
  
# def _get_inumet()

#########################################
#########################################
#########################################

def colorArray(N, band):

  col_seq = getInumetColorRange()

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
