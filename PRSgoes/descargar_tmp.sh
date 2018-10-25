#!/bin/bash

# scp worker_goes@solargate.les.edu.uy:/home/worker_goes/script_NOAA/tmp/* /sat/PRS/dev/PRS-sat/PRSgoes/tmp
rsync -av --stats --progress worker_goes@solargate.les.edu.uy:/home/worker_goes/script_NOAA/tmp_cast/ /sat/PRS/dev/PRS-sat/PRSgoes/tmp/
