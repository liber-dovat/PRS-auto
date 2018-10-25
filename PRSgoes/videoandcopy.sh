#!/bin/bash

scp /sat/prd-sat/PNGs/*C*.png webusr@les.edu.uy:/var/www/html/online/images
scp /sat/prd-sat/PNGs/timestamp.html webusr@les.edu.uy:/var/www/html/online

# borro los frames de la carpeta
#rm /sat/prd-sat/PNGs/C02/mp4/*.png
#rm /sat/prd-sat/PNGs/C04/mp4/*.png
#rm /sat/prd-sat/PNGs/C13/mp4/*.png
# rm /sat/prd-sat/PNGs/B01-FR/mp4/*.png
# rm /sat/prd-sat/PNGs/B01-RP/mp4/*.png

# genero los frames y los videos
/sat/PRS/dev/PRS-sat/PRSgoes/frames_mp4.sh /sat/prd-sat/PNGs/C02/mp4/ C02
#/sat/PRS/dev/PRS-sat/PRSgoes/frames_mp4.sh /sat/prd-sat/PNGs/C04/mp4/ C04
/sat/PRS/dev/PRS-sat/PRSgoes/frames_mp4.sh /sat/prd-sat/PNGs/C13/mp4/ C13

scp /sat/prd-sat/PNGs/C*.mp4 webusr@les.edu.uy:/var/www/html/online/videos
