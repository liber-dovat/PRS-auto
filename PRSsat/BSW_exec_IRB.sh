#!/bin/bash

#Versión 1.0. 10/2016. Rodrigo Alonso Suárez

# PROGRAMAS
main='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/PRSsat_auto_IRB';
libs='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/lib_PRSsat';

# PARAMETROS
folders='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_folders_ALL1';
spatial='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_spatial_IRB1';
imglist='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_imglist_IRB1';
product=('/B02-TX/' '/B02-MK/' '/B03-TX/' '/B03-MK/' '/B04-TX/' '/B04-MK/' '/B06-TX/' '/B06-MK/');

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
    	if [ ! -d $RUTAdes$prod$year ]; then
			mkdir -p $RUTAdes$prod$year;
		fi
		if [ ! -d $RUTAdes'/zIMP'$prod$year ]; then
			mkdir -p $RUTAdes'/zIMP'$prod$year;
		fi
	done
done

echo '=== Compilacion ==============================================================';
gcc -o $libs'.o' -c $libs'.c' -lnetcdf -lm;
gcc -o $main $main'.c' $libs'.o' -lnetcdf -lm;

echo '2016/01/goes13.2016.275.143506.BAND_02.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.275.143506.BAND_03.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.275.143506.BAND_04.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.275.143506.BAND_06.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.277.084518.BAND_02.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.277.084518.BAND_03.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.277.084518.BAND_04.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.277.084518.BAND_06.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.279.123506.BAND_02.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.279.123506.BAND_03.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.279.123506.BAND_04.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/01/goes13.2016.279.123506.BAND_06.nc' >> $imglist; # EMULO DESCARGA NOAA

echo '=== Run ======================================================================';
time $main $folders $spatial $imglist;

echo '=== Borro imglist ============================================================';
echo '' > $imglist;
