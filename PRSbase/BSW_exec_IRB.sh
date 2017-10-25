#!/bin/bash

#Versión 1.0. 10/2016. Rodrigo Alonso Suárez

# PROGRAMAS
main='/rolo/Wsatelite/PRS/dev/PRS-sat/PRSbase/PRSsat_auto_IRB';
libs='/rolo/Wsatelite/PRS/dev/PRS-sat/PRSbase/lib_PRSsat';
#main='/sat/PRS/libs/PRS-sat/PRSbase/PRSsat_auto_IRB';
#libs='/sat/PRS/libs/PRS-sat/PRSbase/lib_PRSsat';

# PARAMETROS
folders='/rolo/Wsatelite/PRS/dev/PRS-sat/data/job_folders_ALL1';
spatial='/rolo/Wsatelite/PRS/dev/PRS-sat/data/job_spatial_IRB1';
imglist='/rolo/Wsatelite/PRS/dev/PRS-sat/data/job_imglist_IRB1';
#folders='/sat/PRS/libs/PRS-sat/data/job_folders_ALL1';
#spatial='/sat/PRS/libs/PRS-sat/data/job_spatial_IRB1';
#imglist='/sat/PRS/libs/PRS-sat/data/job_imglist_IRB1';

# PRODUCTOS
product=('/B02-T2/' '/B02-MK/' '/B03-T3/' '/B03-MK/' '/B04-T4/' '/B04-MK/' '/B06-T6/' '/B06-MK/');

echo '2016/10/goes13.2016.275.143506.BAND_02.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.275.143506.BAND_03.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.275.143506.BAND_04.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.275.143506.BAND_06.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.277.084518.BAND_02.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.277.084518.BAND_03.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.277.084518.BAND_04.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.277.084518.BAND_06.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.279.123506.BAND_02.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.279.123506.BAND_03.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.279.123506.BAND_04.nc' >> $imglist; # EMULO DESCARGA NOAA
echo '2016/10/goes13.2016.279.123506.BAND_06.nc' >> $imglist; # EMULO DESCARGA NOAA

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

echo '=== Run ======================================================================';
time $main $folders $spatial $imglist;

echo '=== Borro imglist ============================================================';
echo '' > $imglist;
