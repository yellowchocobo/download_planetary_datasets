#!/bin/bash

for f in *cubeatt.map.cub;
do
fname="$(cut -d. -f1-1 <<< $f)"
gdal_translate -ot Byte -of GTiff -co bigtiff=if_safer $fname.cubeatt.map.cub $fname.tif
done
