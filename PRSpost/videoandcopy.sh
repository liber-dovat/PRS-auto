#!/bin/bash

scp /sat/prd-sat/PNGs/*BAND_0*.png webusr@les.edu.uy:/var/www/html/satelite/images
scp /sat/prd-sat/PNGs/timestamp.html webusr@les.edu.uy:/var/www/html/satelite

# borro los frames de la carpeta
# rm /sat/prd-sat/PNGs/B04/mp4/*.png
# rm /sat/prd-sat/PNGs/B01-FR/mp4/*.png
# rm /sat/prd-sat/PNGs/B01-RP/mp4/*.png

# genero los frames y los videos
/sat/PRS/libs/PRS-sat/PRSpost/frames_mp4.sh /sat/prd-sat/PNGs/B04/mp4/ BAND_04
/sat/PRS/libs/PRS-sat/PRSpost/frames_mp4.sh /sat/prd-sat/PNGs/B01-FR/mp4/ BAND_01_FR
/sat/PRS/libs/PRS-sat/PRSpost/frames_mp4.sh /sat/prd-sat/PNGs/B01-RP/mp4/ BAND_01_RP

scp /sat/prd-sat/PNGs/*BAND_0*.mp4 webusr@les.edu.uy:/var/www/html/satelite/videos
