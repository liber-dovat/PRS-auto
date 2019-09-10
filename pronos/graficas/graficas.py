#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy    
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from datetime import date
from dateutil.rrule import rrule, MINUTELY
import time

shortmes=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Set','Oct','Nov','Dic']
meses=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']
shortdia=['Lun','Mar','Mie','Jue','Vie','Sab','Dom']

def my_format_function(x, pos=None):
  x = matplotlib.dates.num2date(x)
  dia = x.strftime('%d')
  mes = x.strftime('%m')
  diasem = x.strftime('%u')

  #https://www.tutorialspoint.com/python/time_strptime.htm
  if dia == '01': 
    label = shortmes[int(mes)-1]
  else:
    label = shortdia[int(diasem)-1] + ' ' + x.strftime('%-d')

  return label

# my_format_function

#::::::::::::::::::::::::::::::::

# <tipo:ghi,dhi,temp>, <columna a graficar>, <ruta csv>, <nombre csv>, <ruta png>, <nombre png>
def plotcsv(tipo, columna, csvPath, csvName, pngPath, pngName, pathLogo, estacion, extraDhi=0, extraDni=0):

  # Read data from 'file.dat'
  tabla = numpy.genfromtxt(csvPath + csvName,   # Data to be read
                                delimiter=',',
                                names=True,
                                dtype=None)

  tabla = numpy.unique(tabla)
  tabla = numpy.sort(tabla)

  # imprimo el cabezal de las tablas para tenerlas como referencia en caso de error
  print tabla.dtype.names

  # guardo las distintas columnas en listas independientes
  col1 = tabla['Timestamp']
  col2 = tabla[columna]

  if tipo == 'uv':
    coliuv = tabla['IUV_AV']

  if extraDhi:
    extraColDhi = tabla[extraDhi]

  if extraDni:
    extraColDni = tabla[extraDni]

  # casteo los timestamps a strings
  fecha = [dt.datetime.strptime(date, '%Y/%m/%d %H:%M:%S.%f') for date in col1]

  # en las tablas pueden haber literales
  dato = []
  bag = []
  error_list = []
  j = 0
  for n in col2:
    if n == 'UnderRange' or n == 'OverRange' or n == 'NotYetSet':
      dato.append(-2.)
      error_list.append(j)
    else:
      dato.append(float(n))
      bag.append(float(n))
    j+=1
  # if

  fig = plt.figure()
  ax  = fig.add_subplot(111)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=5)

  # hours = HourLocator(byhour=range(2,23), interval=6)
  hours = HourLocator(byhour=[6,12,18])

  ax.xaxis.set_major_locator(DayLocator(bymonthday=range(1,32)))
  ax.xaxis.set_major_formatter(FuncFormatter(my_format_function))
  ax.xaxis.set_minor_locator(hours)
  ax.xaxis.set_minor_formatter(DateFormatter("%Hhs"))
  ax.tick_params(which='minor', labelsize=4.5)

  # ----------------------

  # seteo fin para el dia de ayer con ultima hora minuto y segundo
  fin = dt.datetime.now() - dt.timedelta(days=1)
  fin = fin.replace(hour=23)
  fin = fin.replace(minute=59)
  fin = fin.replace(second=59)

  # el comienzo del rango es el dia fin menos 7199 minutos
  ini = fin - dt.timedelta(minutes=7199)

  # parche por las diferencias de los timestamps de las medidas
  fin = fin - dt.timedelta(hours=1)
 
  print fin

  new_fecha = []
  new_dato  = []
  err_dato  = []

  print estacion
  print columna
  if (len(col2) != len(error_list)):
    print numpy.floor(numpy.amin(bag))
    print numpy.ceil(numpy.amax(bag))

  if tipo == 'temp':
    # tmin = numpy.floor(numpy.amin(bag))
    # tmax = numpy.ceil(numpy.amax(bag))
    # min_dato = tmin - 1                             # <--
    # err      = min_dato - (tmax - min_dato) / 44
    err = -6.
    min_dato = -5.1
  elif tipo == 'ghi':
    err = -32.
    min_dato = -2.
  elif tipo == 'dhi':
    err = -18.
    min_dato = -2.
  elif tipo == 'dni':
    err = -32.
    min_dato = -2.
  elif tipo == 'uv':
    err = -2.
    min_dato = 0.
  # if

  hay_error = False

  # float('nan')

  i = 0

  if fecha[i] < ini:
    # adelantar i hasta inicio
    while i < len(fecha) and fecha[i].strftime("%Y/%m/%d %H") < ini.strftime("%Y/%m/%d %H"):
      i += 1
    # while
  # if

  for minutal in rrule(MINUTELY, dtstart=ini, until=fin):
    # si existe la entrada de fecha en el csv

    new_fecha.append(minutal)

    if i < len(fecha) and minutal.strftime("%Y/%m/%d %H:%M") == fecha[i].strftime("%Y/%m/%d %H:%M"):
      if i in error_list:
        new_dato.append(float('nan'))
        err_dato.append(err)
        hay_error = True
      else:
        new_dato.append(dato[i])
        err_dato.append(min_dato)

      i += 1
    else: # si no existe esa fecha en el csv
      new_dato.append(float('nan'))
      err_dato.append(err)
      hay_error = True

# #######################

  i = 0

  if fecha[i] < ini:
    # adelantar i hasta inicio
    while i < len(fecha) and fecha[i].strftime("%Y/%m/%d %H") < ini.strftime("%Y/%m/%d %H"):
      i += 1
    # while
  # if

  j = i

  if tipo == 'uv':
    new_iuv  = []
    for minutal in rrule(MINUTELY, dtstart=ini, until=fin):
      # si existe la entrada de fecha en el csv

      if i < len(fecha) and minutal.strftime("%Y/%m/%d %H:%M") == fecha[i].strftime("%Y/%m/%d %H:%M"):
        if i in error_list:
          new_iuv.append(min_dato)
        else:
          new_iuv.append(coliuv[i])

        i += 1
      else: # si no existe esa fecha en el csv
        new_iuv.append(min_dato)

  if extraDhi:
    newExtraDhi = []
    for minutal in rrule(MINUTELY, dtstart=ini, until=fin):
      # si existe la entrada de fecha en el csv

      if i < len(fecha) and minutal.strftime("%Y/%m/%d %H:%M") == fecha[i].strftime("%Y/%m/%d %H:%M"):
        if i in error_list:
          newExtraDhi.append(min_dato)
        else:
          newExtraDhi.append(extraColDhi[i])

        i += 1
      else: # si no existe esa fecha en el csv
        newExtraDhi.append(min_dato)

  if extraDni:
    newExtraDni = []
    for minutal in rrule(MINUTELY, dtstart=ini, until=fin):
      # si existe la entrada de fecha en el csv

      if j < len(fecha) and minutal.strftime("%Y/%m/%d %H:%M") == fecha[j].strftime("%Y/%m/%d %H:%M"):
        if j in error_list:
          newExtraDni.append(min_dato)
        else:
          newExtraDni.append(extraColDni[j])

        j += 1
      else: # si no existe esa fecha en el csv
        newExtraDni.append(min_dato)

  # ----------------------

  if tipo == 'temp':
    # if hay_error:
    #   vmin = numpy.floor(numpy.amin(new_dato))
    # else:
    #   vmin = numpy.floor(numpy.amin(new_dato) - 1)
    # # if
    # vmax = numpy.ceil(numpy.amax(new_dato) + 1)
    vmin = -5
    vmax = 50
  elif tipo == 'ghi':
    vmin = 0
    vmax = 1400
  elif tipo == 'dhi':
    vmin = 0
    vmax = 800
  elif tipo == 'dni':
    vmin = 0
    vmax = 1400
  elif tipo == 'uv':
    vmin = 0
    vmax = 100
  # if

  if tipo == 'temp':
    ylabel = u'Temperatura (ºC)'
    ax.plot_date(new_fecha, new_dato, ls='-', marker="", linewidth=1, color='red', clip_on=False)

    if hay_error:
      # ax.plot_date(new_fecha, err_dato, ls='-', marker="", linewidth=1, color='red', clip_on=False)
      ax.fill_between(new_fecha, err_dato, min_dato, linewidth=0, facecolor='red', alpha=1, clip_on=False, zorder=-100)

  elif tipo == 'uv':
    ylabel = u'Irradiancia UVA (W/m²)'
    ax.plot_date(new_fecha, new_dato, ls='-', marker="", linewidth=0.7, color='#7F00FF', clip_on=False)
    ax.fill_between(new_fecha, 0, new_dato, linewidth=0, facecolor='#b571fa', alpha=0.7, clip_on=False, zorder=-100)

    if hay_error:
      # ax.plot_date(new_fecha, err_dato, ls='-', marker="", linewidth=1, color='red', clip_on=False)
      ax.fill_between(new_fecha, err_dato, 0, linewidth=0, facecolor='red', alpha=1, clip_on=False, zorder=-100)

    ax_iuv = ax.twinx()
    max = numpy.ceil(numpy.amax(new_iuv) + 1)
    ax_iuv.set_ylim([0, max])
    ax_iuv.plot_date(new_fecha, new_iuv, ls='-', marker="", linewidth=0.5, color='red', clip_on=True, zorder=-100)
    ax_iuv.set_ylabel(u"Índice UV", fontsize=7)
    for label in ax_iuv.yaxis.get_majorticklabels():
      label.set_fontsize(5)

  elif extraDhi or extraDni:
    ylabel = u'Irradiancia (W/m²)'
    ax.plot_date(new_fecha, new_dato, ls='-', marker="", linewidth=0.7, color='#3737FF', clip_on=False)
    # ax.fill_between(new_fecha, 0, new_dato, linewidth=0, facecolor='#b571fa', alpha=0.4, clip_on=False, zorder=-100)

    if hay_error:
      # ax.plot_date(new_fecha, err_dato, ls='-', marker="", linewidth=1, color='red', clip_on=False)
      ax.fill_between(new_fecha, err_dato, 0, linewidth=0, facecolor='red', alpha=1, clip_on=False, zorder=-100)

  else:
    ylabel = u'Irradiancia (W/m²)'
    ax.plot_date(new_fecha, new_dato, ls='-', marker="", linewidth=0.7, color='#3737ff', clip_on=False)
    ax.fill_between(new_fecha, 0, new_dato, linewidth=0, facecolor='#bfbfff', alpha=0.7, clip_on=False, zorder=-100)

    if hay_error:
      # ax.plot_date(new_fecha, err_dato, ls='-', marker="", linewidth=1, color='red', clip_on=False)
      ax.fill_between(new_fecha, err_dato, 0, linewidth=0, facecolor='red', alpha=1, clip_on=False, zorder=-100)
  # if

  if extraDni:
    ax_dni = ax.twinx()
    ax_dni.set_ylim([0, vmax])
    ax_dni.plot_date(new_fecha, newExtraDni, ls='-', marker="", linewidth=0.7, color='green', alpha=0.5, clip_on=True, zorder=-100)
    plt.setp(ax_dni.get_yticklabels(), visible=False)

  if extraDhi:
    ax_dhi = ax.twinx()
    ax_dhi.set_ylim([0, vmax])
    ax_dhi.plot_date(new_fecha, newExtraDhi, ls='-', marker="", linewidth=0.7, color='red', alpha=0.5, clip_on=True, zorder=-100)
    plt.setp(ax_dhi.get_yticklabels(), visible=False)

  ax.set_title(estacion.decode('utf-8'), fontsize=8)
  ax.set_xlabel('Fecha', fontsize=7)
  ax.set_ylabel(ylabel, fontsize=7)

  ax.grid(True)
  ax.set_axisbelow(True)
  ax.set_ylim([vmin,vmax])

  # agrego el logo en el documento
  logo = plt.imread(pathLogo)
  plt.figimage(logo, 0, 370)

  if tipo == 'ghi':
    pie = u"Irradiancia global horizontal"
  elif tipo == 'dhi':
    pie = u"Irradiancia difusa horizontal"
  elif tipo == 'dni':
    pie = u"Irradiancia directa normal"
  elif tipo == 'temp':
    pie = u"Temperatura de aire ambiente"
  elif tipo == 'uv':
    pie = u"Irradiancia global horizontal UVA e índice UV"
  # if

  if extraDhi or extraDni:
    fileName = "priv_" + pngName
  else:
    fileName = pngName

  # genero el pie de la imagen, con el logo y la info del archivo
  if extraDhi or extraDni:
    plt.annotate("GHI", (0,0), (-30,-15), color='#3737FF', xycoords='axes fraction', textcoords='offset points', va='top', fontsize=7, family='monospace')

    if extraDhi:
      plt.annotate("DHI", (0,0), (-10,-15), color="red", xycoords='axes fraction', textcoords='offset points', va='top', fontsize=7, family='monospace')
    
    if extraDni:
      plt.annotate("DNI", (0,0), (10,-15), color="green", xycoords='axes fraction', textcoords='offset points', va='top', fontsize=7, family='monospace')

  else:
    plt.annotate(pie, (0,0), (-30,-15), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=7, family='monospace')

  # guardo la imagen en la ruta destino
  fig.set_figheight(1.8)
  fig.set_figwidth(8)
  plt.savefig(pngPath + fileName, bbox_inches='tight', dpi=200, transparent=True) 
  plt.close() # cierro el archivo

# plotcsv

