#!/bin/bash

BANDA=$2
INDIR=$1
OUTDIR="/sat/prd-sat/PNGs/"

echo "genero el repage";
cd $INDIR; convert -crop 950x1160+0+0 +repage ART*.png repage%03d.png;
echo "genero el videos";
cd $INDIR; ffmpeg -y -framerate 5 -i repage%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p $OUTDIR$BANDA.mp4;