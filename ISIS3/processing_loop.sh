#!/bin/bash

# This version of the script is better if limited by space as all the temporary cub files will be removed
# in between each image processed.
for i in *.IMG;
do
  pid="$(cut -d. -f1-1 <<< $i)"
  lronac2isis from=$pid.IMG to=$pid.cub
  spiceinit from=$pid.cub
  lronaccal from=$pid.cub  to=$pid.lvl1.cub
  lronacecho from=$pid.lvl1.cub to=$pid.lvl2.cub
  cam2map from=$pid.lvl2.cub to=$pid.map.cub map=$pid.map matchmap=no pixres=CAMERA defaultrange=MINIMIZE
  stretch from=\$1.map.cub to=\$1.stretch.cub usepercentages=yes pairs="0.:1 0.5:1 99.5:254 100.:254"
  cubeatt from=\$1.stretch.cub to=\$1.cubeatt.map.cub+lsb+tile+attached+unsignedbyte+1:254

  # removing all the cub created except of the last one
  rm $pid.cub
  rm $pid.lvl1.cub
  rm $pid.lvl2.cub
  rm $pid.map.cub
  rm $pid.stretch.cub

  # convert cub to tif file (GDAL part)
  gdal_translate -ot Byte -of GTiff -co bigtiff=if_safer $pid.cubeatt.map.cub $pid.tif

  # removing the last cub files and the *.IMG
  rm $pid.cubeatt.map.cub
  rm $pid.IMG
done

