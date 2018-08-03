#!/bin/bash

#Versión 1.0. 10/2016. Rodrigo Alonso Suárez

# PROGRAMAS
main='/home/ldovat/dev/PRS-sat/PRS-R/PRS_auto_R';
libs='/home/ldovat/dev/PRS-sat/PRS-R/lib_PRSsat';
#main='/sat/PRS/libs/PRS-sat/PRSbase/PRSsat_auto_VIS';
#libs='/sat/PRS/libs/PRS-sat/PRSbase/lib_PRSsat';

# PARAMETROS
folders='/home/ldovat/dev/PRS-sat/PRS-R/data/job_folders_ALL1';
spatial='/home/ldovat/dev/PRS-sat/PRS-R/data/job_spatial_VIS1';
imglist='/home/ldovat/dev/PRS-sat/PRS-R/data/job_imglist_VIS1';
#folders='/sat/PRS/libs/PRS-sat/data/job_folders_ALL1';
#spatial='/sat/PRS/libs/PRS-sat/data/job_spatial_VIS1';
#imglist='/sat/PRS/libs/PRS-sat/data/job_imglist_VIS1';

# PRODUCTOS
product=('/B01-FR/' '/B01-RP/' '/B01-N1/' '/B01-MK/');

echo 'OR_ABI-L2-CMIPF-M3C04_G16_s20180531700392_e20180531711159_c20180531711219.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.277.084518.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.279.123506.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.275.143506.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.277.084518.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.279.123506.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.275.143506.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.277.084518.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.279.123506.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.275.143506.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.277.084518.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA
# echo '2016/10/goes13.2016.279.123506.BAND_01.nc' >> $imglist; # EMULO DESCARGA NOAA

echo '=== Carpetas =================================================================';
j=1;
while read line; do
	if [ $j -eq 2 ]; then
		RUTAsal=$line;
	fi
	let j=$j+1;
done < $folders
j=1;
while read line; do
	if [ $j -eq 9 ]; then
		codigo=$line;
	fi
	let j=$j+1;
done < $spatial
RUTAdes=$RUTAsal$codigo;
if [ ! -d $RUTAdes'/meta/' ]; then
	mkdir -p $RUTAdes'/meta/';
fi
if [ ! -d $RUTAdes'/test/' ]; then
	mkdir -p $RUTAdes'/test/';
fi
if [ ! -d $RUTAdes'/zCRR/' ]; then
	mkdir -p $RUTAdes'/zCRR/';
fi
for line in $(<$imglist); do
	year=${line:15:4};
	#echo $year;
	for prod in ${product[*]}
	do
		#echo $RUTAdes$prod$year;
    if [ ! -d $RUTAdes$prod$year ]; then
			mkdir -p $RUTAdes$prod$year;
		fi
		#echo $RUTAdes'/zIMP'$prod$year;
		if [ ! -d $RUTAdes'/zIMP'$prod$year ]; then
			mkdir -p $RUTAdes'/zIMP'$prod$year;
		fi
	done
done

# echo '=== Compilacion ==============================================================';
# gcc -o $libs'.o' -c $libs'.c' -lnetcdf -lm;
# gcc -o $main $main'.c' $libs'.o' -lnetcdf -lm;

echo '=== Run ======================================================================';
time $main $folders $spatial $imglist;

echo '=== Borro imglist ============================================================';
echo '' > $imglist;
