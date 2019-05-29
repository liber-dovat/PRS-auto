#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
from array import array

#########################################

def llamarScript(scriptpath, parametros):

  # subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/videoandcopy.sh", shell=True)
  # subprocess.call(["ls", "-l"])
  s = subprocess.call(scriptpath + " " + parametros, shell=True)
# llamarScript

#########################################
#########################################

def readFolders(DATAfolders):

  f = open(DATAfolders, "r")
  temp = f.read().splitlines()
  RUTAent = temp[0]
  RUTAsal = temp[1]
  RUTAcal = temp[2]
  f.close()

  return RUTAent, RUTAsal, RUTAcal

# end readFolders

#########################################
#########################################

def readSpatial(DATAspatial):

  f           = open(DATAspatial, "r")
  temp        = f.read().splitlines()
  LATmax      = float(temp[0])
  LATmin      = float(temp[1])
  LONmax      = float(temp[2])
  LONmin      = float(temp[3])
  dLATgri     = float(temp[4])
  dLONgri     = float(temp[5])
  dLATcel     = float(temp[6])
  dLONcel     = float(temp[7])
  CODEspatial = temp[8].rstrip("\n\r")

  f.close()

  return LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, dLATcel, dLONcel, CODEspatial

# end readSpatial

#########################################
#########################################

def generar_grilla(LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri):

  Ci = int(1 + (LATmax - LATmin)/dLATgri)
  Cj = int(1 + (LONmax - LONmin)/dLONgri)
  Ct = Ci*Cj;

  LATvec = [0]*Ci
  LONvec = [0]*Cj
  LATmat = [0]*Ct
  LONmat = [0]*Ct

  for h1 in range(0, Ci):
    LATvec[h1] = LATmin + dLATgri*h1

  for h1 in range(0, Cj):
    LONvec[h1] = LONmin + dLONgri*h1

  # MATRICES DE LATITUD Y LONGITUD
  for h1 in range(0, Ci):
    for h2 in range(0, Cj):
      h3 = (Ci - 1 - h1)*Cj + h2
      LATmat[h3] = LATvec[h1]
      LONmat[h3] = LONvec[h2]
    # end for h2
  # end for h1

  return LATmat, LONmat, LATvec, LONvec, Ci, Cj, Ct

# end generar_grilla

#########################################
#########################################

# https://docs.python.org/3/library/array.html
# Type code C Type             Python Type       Minimum size in bytes   Notes
# 'b'       signed char        int               1    
# 'B'       unsigned char      int               1    
# 'u'       Py_UNICODE         Unicode character 2   (1)
# 'h'       signed short       int               2    
# 'H'       unsigned short     int               2    
# 'i'       signed int         int               2    
# 'I'       unsigned int       int               2    
# 'l'       signed long        int               4    
# 'L'       unsigned long      int               4    
# 'q'       signed long long   int               8   (2)
# 'Q'       unsigned long long int               8   (2)
# 'f'       float              float             4    
# 'd'       double             float             8    

# https://stackoverflow.com/questions/807863/how-to-output-list-of-floats-to-a-binary-file-in-python

# input_file = open('file', 'rb')
# float_array = array('f')
# float_array.fromstring(input_file.read())

def guardar_grilla(RUTAsal, Ci, Cj, PSIlat, dLATgri, PSIlon, dLONgri, LATvec, LONvec, LATmat, LONmat):

  Cmeta = 6;
  SAVE_META = [0.] * Cmeta

  SAVE_META[0] = float(Ci);
  SAVE_META[1] = float(Cj);
  SAVE_META[2] = float(PSIlat);
  SAVE_META[3] = float(dLATgri);
  SAVE_META[4] = float(PSIlon);
  SAVE_META[5] = float(dLONgri);

  RUTAmeta    = RUTAsal + "meta/T000gri.META"
  RUTA_LATvec = RUTAsal + "meta/T000gri.LATvec"
  RUTA_LONvec = RUTAsal + "meta/T000gri.LONvec"
  RUTA_LATmat = RUTAsal + "meta/T000gri.LATmat"
  RUTA_LONmat = RUTAsal + "meta/T000gri.LONmat"

  # RUTAmeta
  output_file = open(RUTAmeta, 'wb')
  float_array = array('f', SAVE_META)
  float_array.tofile(output_file)
  output_file.close()

  # RUTA_LATvec
  output_file = open(RUTA_LATvec, 'wb')
  float_array = array('f', LATvec)
  float_array.tofile(output_file)
  output_file.close()

  # RUTA_LONvec
  output_file = open(RUTA_LONvec, 'wb')
  float_array = array('f', LONvec)
  float_array.tofile(output_file)
  output_file.close()

  # RUTA_LATmat
  output_file = open(RUTA_LATmat, 'wb')
  float_array = array('f', LATmat)
  float_array.tofile(output_file)
  output_file.close()

  # RUTA_LONmat
  output_file = open(RUTA_LONmat, 'wb')
  float_array = array('f', LONmat)
  float_array.tofile(output_file)
  output_file.close()

# end guardar_grilla

def cargar_calibracion_VIS(RUTAcal, satelite):

  PreFile = RUTAcal + "B01_GOES" + satelite + "pre"
  PosFile = RUTAcal + "B01_GOES" + satelite + "pos"

  pre_file = open(PreFile, 'r')
  ARCHste = int  (pre_file.readline())
  M       = float(pre_file.readline())
  Xspace  = float(pre_file.readline())
  K       = float(pre_file.readline())
  pre_file.close()
  # if (ARCHste != satelite){printf("No se pudo verificar el CHK PRE. Cerrando.\n"); return 0;}

  pos_file = open(PosFile, 'r')
  ARCHste = int(pos_file.readline())
  yea_doy = pos_file.readline().rstrip("\n\r").split(" ")
  iniYEA  = int(yea_doy[0])
  iniDOY  = (yea_doy[1])
  alfa    = float(pos_file.readline())
  beta    = float(pos_file.readline())
  pos_file.close()
  # if (ARCHste != satelite){printf("No se pudo verificar el CHK PRE. Cerrando.\n"); return 0;}

  return iniYEA, iniDOY, Xspace, M, K, alfa, beta

# end cargar_calibracion_VIS
