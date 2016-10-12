#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import struct
import numpy

# RUTAsat = '/sat/prd-sat/ART_G015x015GG_C015x015/'
# PATHfr  = RUTAsat + 'B01-FR/2016/ART_2016275_143500.FR'

# print PATHfr

RUTAsat = './test_fr/'
PATHpng = RUTAsat + 'png/'
PATHfr  = RUTAsat + 'B01-FR/2016/ART_2016285_133500.FR'

fid = open(RUTAsat + 'meta/T000gri.META', 'r')
meta = numpy.fromfile(fid, dtype='float32')
fid.close()

fid = open(RUTAsat + 'meta/T000gri.LATvec', 'r')
LATdeg_vec = numpy.fromfile(fid, dtype='float32')
LATdeg_vec = LATdeg_vec[::-1] # invierto el arreglo porque quedaba invertido verticalmente
fid.close()

fid = open(RUTAsat + 'meta/T000gri.LONvec', 'r')
LONdeg_vec = numpy.fromfile(fid, dtype='float32')
fid.close()

# obtengo del vector meta el largo y alto de elementos de los vectores y los datos
Ci = meta[0];
Cj = meta[1];
Ct = Ci*Cj;

print "Lon min:" + str(numpy.amin(LONdeg_vec)) + ", Lon max:" + str(numpy.amax(LONdeg_vec))
print "Lat min:" + str(numpy.amin(LATdeg_vec)) + ", Lat max:" + str(numpy.amax(LATdeg_vec))

# imagen
fid = open(PATHfr, 'r')
data = numpy.fromfile(fid, dtype='float32')
fid.close()
IMG1 = numpy.reshape(data, (Ci, Cj))
print IMG1.shape

cs = plt.pcolormesh(LONdeg_vec, LATdeg_vec, IMG1, cmap='jet')

# agrego el colorbar
cbar = plt.colorbar(cs)

plt.savefig(PATHpng + 'file.png', bbox_inches='tight', dpi=200)
plt.close()

# % --- imagen
# fid = fopen(PATHfr, 'r');
# data = fread(fid, Ct, 'float32');
# fclose(fid);
# IMG1 = reshape(data, Cj, Ci);

# figure(1)
# imagesc(LONdeg_vec, LATdeg_vec, flipud(IMG1'));
# view(2); shading interp; axis tight; axis xy;
# colorbar;
