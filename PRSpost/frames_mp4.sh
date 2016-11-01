#!/bin/bash

BANDA=$2
INDIR=$1
OUTDIR="/sat/prd-sat/PNGs/"

convert -crop 948x1132+0+0 +repage $INDIR*.png $INDIRrepage%03d.png
ffmpeg -framerate 5 -i $INDIRrepage%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p $OUTDIR$BANDA.mp4