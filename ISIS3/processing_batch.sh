#!/bin/bash

# This version of the script process all the image at the same time (i.e., conducting the first for all images
# and then so forth until the end). This is nice
ls -1 *.IMG | cut -d. -f1 > nac.lis

lronac2isis from=\$1.IMG to=\$1.cub -batchlist=nac.lis
spiceinit from=\$1.cub -batchlist=nac.lis
lronaccal from=\$1.cub  to=\$1.lvl1.cub -batchlist=nac.lis
lronacecho from=\$1.lvl1.cub to=\$1.lvl2.cub -batchlist=nac.lis
cam2map from=\$1.lvl2.cub to=\$1.map.cub map=\$1.map matchmap=no pixres=CAMERA defaultrange=MINIMIZE -batchlist=nac.lis
stretch from=\$1.map.cub to=\$1.stretch.cub usepercentages=yes pairs="0.:1 0.5:1 99.5:254 100.:254" -batchlist=nac.lis
cubeatt from=\$1.stretch.cub to=\$1.cubeatt.map.cub+lsb+tile+attached+unsignedbyte+1:254 -batchlist=nac.lis

# removing all the cub created except of the last one
rm *E.cub
rm *.lvl1.cub
rm *.lvl2.cub
rm *.map.cub
rm *.stretch.cub

# convert cub to tif file (GDAL part)
for f in *cubeatt.map.cub;
do
  fname="$(cut -d. -f1-1 <<< $f)"
  gdal_translate -ot Byte -of GTiff -co bigtiff=if_safer $fname.cubeatt.map.cub $fname.tif
done

# removing the last cub files and the *.IMG
rm *.cubeatt.map.cub
rm *.IMG