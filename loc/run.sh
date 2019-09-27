#!/bin/bash

SCRIPT='/sat/PRS/dev/PRS-sat/loc/batchLoc.py'
ESTACIONES='/sat/loc-sat/meta/ZZ_estaciones_all'
DIR_SALIDA='/sat/loc-sat/'

VENTANAS=('0.015' '0.025' '0.050' '0.060' '0.100' '0.150' '0.200' '0.250' '0.300' '0.350' '0.400' '0.450' '0.500' '0.600' '0.700' '0.800' '0.900')

for val in "${VENTANAS[@]}"
do
  time $SCRIPT /sat/art-sat/ART_G015x015UY_C015x015/ $DIR_SALIDA $ESTACIONES $val $val 2000 2009
  time $SCRIPT /sat/art-sat/ART_G015x015EX_C015x015/ $DIR_SALIDA $ESTACIONES $val $val 2010 2015
  time $SCRIPT /sat/art-sat/ART_G015x015GG_C015x015/ $DIR_SALIDA $ESTACIONES $val $val 2016 2017
done
