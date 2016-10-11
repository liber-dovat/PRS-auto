#!/usr/bin/python

import struct
import numpy

# RUTAsat = '/sat/prd-sat/ART_G015x015GG_C015x015/'
# PATHfr  = RUTAsat + 'B01-FR/2016/ART_2016275_143500.FR'

# print PATHfr

RUTAsat = './test_fr/'

'''
% --- Cargar metadatos
fid = fopen([RUTAsat,'meta/T000gri.META'], 'r');
meta = fread(fid, 6, 'float32');
fclose(fid);
fid = fopen([RUTAsat,'meta/T000gri.LATvec'], 'r');
LATdeg_vec = fread(fid, meta(1), 'float32');
fclose(fid);
fid = fopen([RUTAsat,'meta/T000gri.LONvec'], 'r');
LONdeg_vec = fread(fid, meta(2), 'float32');
fclose(fid);

Ci = meta(1);
Cj = meta(2);
Ct = Ci*Cj;
'''

fid = open(RUTAsat + 'meta/T000gri.META', 'rb')
meta = numpy.fromfile(fid, dtype='float32')
fid.close()

fid = open(RUTAsat + 'meta/T000gri.LATvec', 'r')
LATdeg_vec = numpy.fromfile(fid, dtype='float32')
fid.close()

fid = open(RUTAsat + 'meta/T000gri.LONvec', 'r')
LONdeg_vec = numpy.fromfile(fid, dtype='float32')
fid.close()

print meta
print LATdeg_vec
print LONdeg_vec

print meta.size
print LATdeg_vec.size
print LATdeg_vec.size
