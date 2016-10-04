#!/bin/bash

#Versión 1.0	03/02/2014	Rodrigo Alonso Suárez

main='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/PRSsat_auto';
libs='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/lib_PRSsat';
folders='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_folders_001';
spatial='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_spatial_001';
imglist='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_imglist_001';
product=('/B01-FR/' '/B01-RP/' '/B01-N1/' '/B01-MK/' '/B02-TX/' '/B02-MK/' '/B03-TX/' '/B03-MK/' '/B04-TX/' '/B04-MK/' '/B06-TX/' '/B06-MK/');

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
	year=${line:7:4};
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