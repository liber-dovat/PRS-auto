#!/bin/bash

# INDIR: Directorio donde se encuentras los archivos png
# BANDA: Nombre de la banda, y se utiliza para crear el nombre del archivo

BANDA=$2
INDIR=$1
OUTDIR="/sat/prd-sat/PNGs/"

echo "genero el repage";
cd $INDIR; convert -background "#4F7293" -alpha remove -geometry 1000x1222 -crop 998x1212+0+0 +repage C*.png repage%03d.png;
echo "genero el video en mp4";
cd $INDIR; ffmpeg -y -framerate 5 -i repage%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p $OUTDIR$BANDA.mp4;
# echo "genero el video en webm";
# cd $INDIR; ffmpeg -i $OUTDIR$BANDA.mp4 -vcodec libvpx-vp9 -b:v 1M $OUTDIR$BANDA.webm;
