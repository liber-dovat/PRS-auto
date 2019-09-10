#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy
import math
import datetime as dt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from open_csv import getCsvCols, cosSolarZenithAngle

import locale
locale.setlocale(locale.LC_ALL, '')

# http://stackoverflow.com/questions/20033396/how-to-visualize-95-confidence-interval-in-matplotlib
# http://stackoverflow.com/questions/27164114/show-confidence-limits-and-prediction-limits-in-scatter-plot
# http://matplotlib.org/1.2.1/examples/pylab_examples/errorbar_demo.html
# http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.errorbar.html

#########################################
#########################################
#########################################

# Datos en solargate:/datos01/drop-RMCIS/ZZ_minutal/AZ/AZ_DT_20181203T183700.csv

# Yo uso estos vectores en python. Lo que pueden hacer es generar un archivo .txt en donde en cada línea haya solamente los valores separados por comas a graficar:

# desvio_up       = [fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,289,558,528,301,106,0,0,0,0,0]
# pronostico      = [fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,219,478,458,231,36,-4,-4,-4,-3,-4]
# desvio_down     = [fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,149,408,388,161,-46,0,0,0,0,0]
# reales_up       = [ 0, 0, 0, 0, 0, 0, 0, 0,113,307,597,743,794,837,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn]
# medidas_reales  = [-2,-2,-3,-2,-3,-3,-3,-1, 53,247,537,673,734,767,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn]
# reales_down     = [0,0,0,0,0,0,0,0,-23,177,447,603,664,697,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn]
# hora_pronostico = "14:30"

def plotGhiCz(lat, lon, medidas_reales, pngPath, pngName):

  base = dt.datetime.now()

  # base = dt.datetime.now() - dt.timedelta(days=1)
  base = base.replace(hour=0)
  base = base.replace(minute=5)
  base = base.replace(second=0)
  base = base.replace(microsecond=0)

  minutos = [float('nan')]*144
  csza    = [float('nan')]*144

  for i in range(144):
    minutos[i] = base + dt.timedelta(minutes=i*10)
    csza[i]    = cosSolarZenithAngle(lat, lon, minutos[i])
    if csza[i] < 0:
      csza[i] = 0
    else:
      csza[i] = csza[i]#*1000.0

  fig = plt.figure()
  ax  = fig.add_subplot(111)

  ax.plot(csza, medidas_reales, ls='-', marker="", linewidth=1, color='blue', zorder=100)

  plt.xticks(fontsize=5)
  plt.yticks(fontsize=5)

  ax.tick_params(which='minor', labelsize=4.5)

  ax.set_xlabel(u'CZ', fontsize=7)
  ax.set_ylabel(u'Irradiancia (Wh/m²)', fontsize=7)

  # vmin = 0
  # vmax = 1400

  ax.grid(True)
  ax.set_axisbelow(True)
  # ax.set_ylim([vmin,vmax])

  # guardo la imagen en la ruta destino
  fig.set_figheight(1.8)
  fig.set_figwidth(8)
  plt.savefig(pngPath + pngName, bbox_inches='tight', dpi=200) #, transparent=True
  plt.close() # cierro el archivo

# plotGhiCz

def plotpronos(lat, lon, pronostico, desvio_up, desvio_down, medidas_reales, reales_up, reales_down, hora_pronos, pngPath, pngName, pathLogo):

  base = dt.datetime.now()

  # base = dt.datetime.now() - dt.timedelta(days=1)
  base = base.replace(hour=0)
  base = base.replace(minute=5)
  base = base.replace(second=0)
  base = base.replace(microsecond=0)

  minutos = [float('nan')]*144
  csza    = [float('nan')]*144

  for i in range(144):
    minutos[i] = base + dt.timedelta(minutes=i*10)
    csza[i]    = cosSolarZenithAngle(lat, lon, minutos[i])
    if csza[i] < 0:
      csza[i] = 0
    else:
      csza[i] = csza[i]*1000.0

  hora_actual = 0 # hora_actual queda determinada en función del valor final de medidas_reales

  for r in medidas_reales:
    if math.isnan(r):
      break
    else:
      hora_actual +=1
      # print r

  hora_actual -= 1

  if hora_actual >= 0:
    pronostico[hora_actual]  = medidas_reales[hora_actual]
    desvio_up[hora_actual]   = reales_up[hora_actual]
    desvio_down[hora_actual] = reales_down[hora_actual]

  fig = plt.figure()
  ax  = fig.add_subplot(111)
  plt.xticks(fontsize=5)
  plt.yticks(fontsize=5)

  hours = HourLocator(byhour=range(24))

  ax.xaxis.set_major_locator(hours)
  ax.xaxis.set_major_formatter(DateFormatter("%H"))
  ax.tick_params(which='minor', labelsize=4.5)

  if hora_actual >= 0:
    # linea de hora actual
    ax.plot_date([minutos[hora_actual], minutos[hora_actual]], [0, 1400], 'k-', lw=0.5, zorder=110)
    # marcador de flecha de hora actual
    ax.plot_date(minutos[hora_actual], [-20], 'g^', markersize=4, markeredgewidth=0, alpha=0.8, zorder=115, clip_on=False)

    ax.plot_date(minutos, medidas_reales, ls='-', marker="", linewidth=2, color='blue', zorder=100)
    ax.plot_date(minutos, reales_up, ls='-', marker="", linewidth=1, color='#ff7619', alpha=0.5)
    ax.plot_date(minutos, reales_down, ls='-', marker="", linewidth=1, color='#ff7619', alpha=0.5)
    ax.fill_between(minutos, reales_up, reales_down, linewidth=0, facecolor='#ffb27e', alpha=0.3, zorder=-10)
  # if

  ax.plot_date(minutos, pronostico, ls='-', marker="", linewidth=2, color='red', zorder=90)
  ax.plot_date(minutos, csza, ls='-', marker="", linewidth=1, color='red', zorder=95)

  ax.plot_date(minutos, desvio_up, ls='-', marker="", linewidth=1, color='red', alpha=0.5)
  ax.plot_date(minutos, desvio_down, ls='-', marker="", linewidth=1, color='red', alpha=0.5)
  ax.fill_between(minutos, desvio_up, desvio_down, linewidth=0, facecolor='red', alpha=0.2, zorder=-10)

  plt.suptitle(u"Pronóstico de irradiación global en plano horizontal (GHI)", y=1.07, fontsize=8)
  ax.set_title(u"Estación Montevideo (AZ) ubicada en la Facultad de Ingeniería de UdelaR", x=0.485, fontsize=6)
  ax.set_xlabel(u'Hora del día', fontsize=7)
  ax.set_ylabel(u'Irradiación horaria (Wh/m²)', fontsize=7)

  vmin = 0
  vmax = 1400
  # vmax = 150

  ax.grid(True)
  ax.set_axisbelow(True)
  ax.set_ylim([vmin,vmax])

  # agrego el logo en el documento
  logo = plt.imread(pathLogo)
  plt.figimage(logo, 0, 10)

  dia = dt.datetime.now()

  # plt.annotate("Generado el " + dia.strftime("%d/%m/%Y") + " " + hora_pronos, (0,0), (352,113), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=6)
  plt.annotate("Generado el " + dia.strftime("%d/%m/%Y %H:%M"), (0,0), (352,-21), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=6)

  # legend
  plt.annotate(u'Azul: irradiación real', (0,0), (20,-15), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=5)
  plt.annotate(u'Rojo: Irradiación pronosticada', (0,0), (20,-21), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=5)
  plt.annotate(u'Naranja: intervalo de confianza anterior', (0,0), (20,-28), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=5)

  # guardo la imagen en la ruta destino
  fig.set_figheight(1.8)
  fig.set_figwidth(8)
  plt.savefig(pngPath + pngName, bbox_inches='tight', dpi=200) #, transparent=True
  plt.close() # cierro el archivo

# plotpronos

fn = float('nan')

logo_path = "./logo_grafica_150.png"

medidas_reales = getCsvCols('datos_AZ/*.csv')

# desvio_up   = [fn]*144
# pronostico  = [fn]*144
# desvio_down = [fn]*144

reales_up   = [fn]*144
reales_down = [fn]*144

desvio_up      = [fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
pronostico     = [fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
desvio_down    = [fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
# reales_up      = [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn]
# reales_down    = [-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,72,72,72,72,72,72,72,72,72,72,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn,fn]
# print len(desvio_up)
# print len(pronostico)
# print len(desvio_down)
# print len(reales_up)
# print len(medidas_reales)
# print len(reales_down)
# desvio_up = desvio_up*15
# desvio_down = desvio_down*15
# reales_up = reales_up*15
# reales_down = reales_down*15

AZ_lat = -34.918224
AZ_lon = -56.16653

plotpronos(AZ_lat, AZ_lon, pronostico, desvio_up, desvio_down, medidas_reales, reales_up, reales_down, "14:30", './', 'pronos.png', logo_path)
# plotGhiCz(AZ_lat, AZ_lon, medidas_reales, './', 'ghi_cz.png')
