#!/bin/sh

module load GDAL/3.3.0-foss-2021a

# convert cub to tif file (GDAL part)
for f in *cubeatt.map.cub;
do
  fname="$(cut -d. -f1-1 <<< $f)"
  gdal_translate -ot Byte -of GTiff -co bigtiff=if_safer $fname.cubeatt.map.cub $fname.tif
done