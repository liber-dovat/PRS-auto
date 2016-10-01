#!/usr/bin/python

import os
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from   os      import listdir
from   os.path import isfile, join, basename

# imagen a procesar
#PATHimg = '/rolo/WSolar/standalones/procesar_NetCDFs/data/goes13.2016.245.114518.BAND_01.nc';
PATHimg = '/rolo/WSolar/standalones/procesar_NetCDFs/data/goes13.2016.274.143507.BAND_01.nc';

# proyeccion regular
LATmax =  10; LATmin = -40; dLATgri = 1; dLATcel = 1; # proyeccion regular en latitud
LONmax = -30; LONmin = -85; dLONgri = 1; dLONcel = 1; # proyeccion regular en longitud

############## CARGAR NETCDF

nc_fid = netCDF4.Dataset(PATHimg, 'r');
lats_mat = nc_fid.variables['lat'][:];
lons_mat = nc_fid.variables['lon'][:];
data_mat = nc_fid.variables['data'][:];
band_mat = nc_fid.variables['bands'][:];
nc_fid.close();

############## OPERACIONES SOBRE EL NETCDF

# vectorizo datos del NetCDF
lats_mat = np.array(lats_mat, dtype=np.float64); # por las dudas
lons_mat = np.array(lons_mat, dtype=np.float64); # por las dudas
data_mat = np.array(data_mat, dtype=np.float64); # por las dudas
lats_vec = lats_mat.ravel(); # vectoriza la matriz
lons_vec = lons_mat.ravel(); # vectoriza la matriz
data_vec = data_mat.ravel(); # vectoriza la matriz
lats_vec = np.array(lats_vec, dtype=np.float64); # por las dudas
lons_vec = np.array(lons_vec, dtype=np.float64); # por las dudas
data_vec = np.array(data_vec, dtype=np.float64); # por las dudas

# mascaras OKs
MSKvec_fail = (np.abs(lats_vec)>100)|(np.abs(lons_vec)>100)|(data_vec<=0);
lats_vec[MSKvec_fail] = 500; # valor grande (mayor a 360)
lons_vec[MSKvec_fail] = 500; # valor grande (mayor a 360)
data_vec[MSKvec_fail] = -1; # valor imposible
Ct = len(data_vec);
print(Ct)

############## PASAR A PROYECCION REGULAR

# vectores de latitud y longitud regular
LATmax = np.float64(LATmax); LATmin = np.float64(LATmin);
LONmax = np.float64(LONmax); LONmin = np.float64(LONmin);
dLATgri = np.float64(dLATgri); dLATcel = np.float64(dLATcel);
dLONgri = np.float64(dLONgri); dLONcel = np.float64(dLONcel);
LATvec = np.arange(LATmin, LATmax+1e-14, dLATgri, dtype=np.float64); #fuck arange() endpoint!
LONvec = np.arange(LONmin, LONmax+1e-14, dLATgri, dtype=np.float64); #fuck arange() endpoint!
n = len(LATvec); # i
m = len(LONvec); # j

# matriz regular de datos de satelite
DATmat = np.zeros((n, m), dtype=np.float64); # crea array de tamano mxn, inicia en 0.
LATmat = np.zeros((n, m), dtype=np.float64); # crea array de tamano mxn, inicia en 0.
LONmat = np.zeros((n, m), dtype=np.float64); # crea array de tamano mxn, inicia en 0.
MSKmat = np.zeros((n, m), dtype=np.int); # crea array de tamano mxn, inicia en 0.
CNTmat = np.zeros((n, m), dtype=np.int); # crea array de tamano mxn, inicia en 0.

# PRUEBA 1: regularizacion. MUY lenta. IMG 80 MB 1x1 en 1min 26.
# for i in range(0, n): # procesa entre 0 y (n-1)
#   MSKlat = (lats_vec>=(LATvec[i] - (dLATcel/2)))&(lats_vec<=(LATvec[i] + (dLATcel/2)));
#   print('Procesando linea %d de %d' % (i+1, n));
#   for j in range(0, m): # procesa entre 0 y (m-1)
#     LATmat[n-i-1,j] = LATvec[i];
#     LONmat[n-i-1,j] = LONvec[j];
#     MSKk = MSKlat&(lons_vec>=(LONvec[j] - (dLONcel/2)))&(lons_vec<=(LONvec[j] + (dLONcel/2)))&(data_vec>0);
#     Cok = np.sum(MSKk);
#     if Cok > 0:
#       DATmat[n-i-1,j] = np.mean(data_vec[MSKk]);
#       MSKmat[n-i-1,j] = 1;
#       CNTmat[n-i-1,j] = Cok;

# PRUEBA 2: regularizacion. SOLO ESTO DEMORA 1 MINUTO!!!
for k in range(0, Ct): # procesa entre 0 y (Ct-1)
  MSKlat_k = (lats_vec[k]<LATmax+(dLATcel/2))&(lats_vec[k]>LATmin-(dLATcel/2));
  MSKlon_k = (lons_vec[k]<LONmax+(dLONcel/2))&(lons_vec[k]>LONmin-(dLONcel/2));
  MSKk = (data_vec[k] > 0)&MSKlat_k&MSKlon_k;
  if MSKk == 1:
    jm = k;
    #print('Procesando linea %d de %d' % (i+1, n));

# print(DATmat)
# print(LATmat)
# print(LONmat)
# print(LATvec)
# print(LONvec)

# plt.imshow(DATmat)
# plt.show()

# MSK = (LATvec == -30);
# lat = LATvec[MSK];
# print(MSK)
# print(LATvec)
# print(lat)
# print(LONvec)
# print(DATmat[0,0])
# print(DATmat[0,:])
# print(DATmat[:,0])
# print(n)
# print(m)