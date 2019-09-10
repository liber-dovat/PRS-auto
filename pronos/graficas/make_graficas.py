#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime as dt
from graficas import plotcsv

# def plotcsv(tipo, columna, csvPath, csvName, pngPath, pngName, pathLogo, estacion):

logo_path = "/home/worker_med/scripts/graficas_png/logo_grafica_100.png"
csv_path = "/home/worker_med/scripts/graficas_tmp/"
png_path = "/home/worker_med/scripts/graficas_png/"

estacion = ""
csv_name = ""

# Antártida

# "Timestamp"          1
# "TZ"                 2
# "GHI1_AV (W/mV)"     3
# "GHI2_AV (W/m2)"     4
# "TA_AV (deg C)"      5
# "TLogger_AV (deg C)" 6
# "VBAT_EXT_AV (volt)" 7
# "UVA_AV (W/m2)"      8
# "UVE_AV (W/m2)"      9
# "TUVA_AV (deg C)"    10
# "UVB_AV (W/m2)"      11
# "TUVB_AV (deg C)"    12
# "IUV_AV"             13
def ba(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_WmV", csv_path, csv_name, png_path, "ba_ghi.png", logo_path, estacion)
  plotcsv("uv", "UVA_AV_Wm2", csv_path, csv_name, png_path, "ba_uv.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "ba_temp.png", logo_path, estacion)
# ba

# Artigas
def ar(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "ar_ghi.png", logo_path, estacion)
  #plotcsv("dhi", "DHI_AV_Wm2", csv_path, csv_name, png_path, "ar_dhi.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "ar_temp.png", logo_path, estacion)

  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "ar_ghi.png", logo_path, estacion, extraDhi="DHI_AV_Wm2", extraDni="DNI_AV_Wm2")
# ar

# Canelones
def lb(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "lb_ghi.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "lb_temp.png", logo_path, estacion)
# lb

# Colonia
def zu(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "zu_ghi.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "zu_temp.png", logo_path, estacion)
# zu

# Montevideo
def az(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "az_ghi.png", logo_path, estacion)
  plotcsv("temp", "Temperatura_TP1000_AV_C", csv_path, csv_name, png_path, "az_temp.png", logo_path, estacion)
# az

# Rocha
def rc(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "rc_ghi.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "rc_temp.png", logo_path, estacion)
# rc

# Salto
def le(estacion, csv_name):
  plotcsv("ghi", "GHI1_Wm2", csv_path, csv_name, png_path, "le_ghi.png", logo_path, estacion)
  #plotcsv("dhi", "DHI_Wm2", csv_path, csv_name, png_path, "le_dhi.png", logo_path, estacion)
  #plotcsv("dni", "DNI1_Wm2", csv_path, csv_name, png_path, "le_dni.png", logo_path, estacion)
  plotcsv("temp", "TA_deg_C", csv_path, csv_name, png_path, "le_temp.png", logo_path, estacion)

  plotcsv("ghi", "GHI1_Wm2", csv_path, csv_name, png_path, "le_ghi.png", logo_path, estacion, extraDhi="DHI_Wm2", extraDni="DNI1_Wm2")
# le

# Tacuarembó
def ta(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "ta_ghi.png", logo_path, estacion)
  #plotcsv("dhi", "DHI_AV_Wm2", csv_path, csv_name, png_path, "ta_dhi.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "ta_temp.png", logo_path, estacion)

  #plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "ta_ghi.png", logo_path, estacion, extraDhi="DHI_AV_Wm2")
# ta

# TG
def tg(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "tg_ghi.png", logo_path, estacion)
  #plotcsv("dhi", "DHI_AV_Wm2", csv_path, csv_name, png_path, "tg_dhi.png", logo_path, estacion)
  #plotcsv("dni", "DNI_AV_Wm2", csv_path, csv_name, png_path, "tg_dni.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "tg_temp.png", logo_path, estacion)

  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "tg_ghi.png", logo_path, estacion, extraDhi="DHI_AV_Wm2", extraDni="DNI_AV_Wm2")
# ta


# Treinta y Tres
def pp(estacion, csv_name):
  plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "pp_ghi.png", logo_path, estacion)
  #plotcsv("dhi", "DHI1_AV_Wm2", csv_path, csv_name, png_path, "pp_dhi.png", logo_path, estacion)
  plotcsv("temp", "TA_AV_deg_C", csv_path, csv_name, png_path, "pp_temp.png", logo_path, estacion)

  #plotcsv("ghi", "GHI1_AV_Wm2", csv_path, csv_name, png_path, "pp_ghi.png", logo_path, estacion, extraDhi="DHI1_AV_Wm2")
# pp

# ba("Estación Antártida", "datosBA.csv")
ar("Estación Artigas", "datosAR.csv")
lb("Estación Las Brujas", "datosLB.csv")
zu("Estación Estanzuela", "datosZU.csv")
az("Estación FING", "datosAZ.csv")
#rc("Estación Rocha", "datosRC.csv")
le("Estación LES (Salto)", "datosLE.csv")
ta("Estación Tacuarembó", "datosTA.csv")
#tg("Estación Tomás Gomensoro", "datosTG.csv")
pp("Estación Treinta y Tres", "datosPP.csv")
rc("Estación Rocha", "datosRC.csv")

