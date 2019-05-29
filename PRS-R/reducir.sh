#!/bin/bash

# ls OR_ABI-L2-CMIPF-M3C01_G16_s2018001*.nc | wc -l
# 96

# ls OR_ABI-L2-CMIPF-M3C02_G16_s2018001*.nc | wc -l
# 96

# ncks -d x,3015,4145   -d y,3852,4764    $nc_04 -O $dest'band04.nc'
# ncks -d x,3015,4145   -d y,3852,4764    $nc_08 -O $dest'band08.nc'
# ncks -d x,3015,4145   -d y,3852,4764    $nc_09 -O $dest'band09.nc'
# ncks -d x,3015,4145   -d y,3852,4764    $nc_10 -O $dest'band10.nc'
# ncks -d x,3015,4145   -d y,3852,4764    $nc_12 -O $dest'band12.nc'
# ncks -d x,3015,4145   -d y,3852,4764    $nc_13 -O $dest'band13.nc'
# ncks -d x,5935,8365   -d y,7611,9625    $nc_01 -O $dest'band01.nc'
# ncks -d x,11870,16730 -d y,15223,19250  $nc_02 -O $dest'band02.nc'

INDIR='/sat/goesr-sat/2018/C01/'
DEST='/sat/goesr-sat/2018/C01/small/'
PRE='2018small_'
BASENAME='OR_ABI-L2-CMIPF-M3C01_G16_s2018'
FILES=''

# for f in OR_ABI-L2-CMIPF-M3C02_G16_s2018001*.nc; do
#   ncks -d x,11870,16730 -d y,15223,19250 $f -O $DEST$PRE$f
# done
# printf "%03d " {0..100}
cd $INDIR;
for f in `printf "%03d " {1..31}`; do
  LS=`ls $BASENAME$f*.nc`
  FILES=$FILES$LS
  FILES=$FILES" "
done

# echo $FILES

for f in $FILES; do
  if [ ! -f $DEST$PRE$f ]; then
    # ncks -d x,11870,16730 -d y,15223,19250 $f -O $DEST$PRE$f
    ncks -d x,5935,8365   -d y,7611,9625 $f -O $DEST$PRE$f
  fi
done
