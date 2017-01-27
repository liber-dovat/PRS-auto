#!/bin/bash

# INDIR: Directorio donde se encuentras los archivos png
# BANDA: Nombre de la banda, y se utiliza para crear el nombre del archivo

BANDA=$2
INDIR=$1
OUTDIR="/sat/prd-sat/PNGs/"

echo "genero el repage";
cd $INDIR; convert -background "#4F7293" -alpha remove -crop 950x1170+0+0 +repage ART*.png repage%03d.png;
echo "genero el video en mp4";
cd $INDIR; ffmpeg -y -framerate 3 -i repage%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p $OUTDIR$BANDA.mp4;
# echo "genero el video en webm";
# cd $INDIR; ffmpeg -i $OUTDIR$BANDA.mp4 -vcodec libvpx-vp9 -b:v 1M $OUTDIR$BANDA.webm;
