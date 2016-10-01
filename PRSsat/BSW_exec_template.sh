#!/bin/bash

#Versión 1.0	03/02/2014	Rodrigo Alonso Suárez

main='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/PRSsat_auto';
data='/rolo/Wsate/PRS/server-sat-01/libs/PRS-auto/PRSsat/data/job_specs_001';

gcc -o $main $main'.c'

time $main $data