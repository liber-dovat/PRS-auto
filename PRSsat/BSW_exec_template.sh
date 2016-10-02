#!/bin/bash

#Versión 1.0	03/02/2014	Rodrigo Alonso Suárez

main='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/PRSsat_auto';
libs='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/lib_PRSsat';
data='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_specs_001';

gcc -o $libs'.o' -c $libs'.c' -lnetcdf;
gcc -o $main $main'.c' $libs'.o' -lnetcdf;

time $main $data;