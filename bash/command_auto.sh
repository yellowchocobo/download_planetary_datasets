#!/bin/bash

ls -1 *.IMG | cut -d. -f1 > nac.lis

lronac2isis from=\$1.IMG to=\$1.cub -batchlist=nac.lis
spiceinit from=\$1.cub -batchlist=nac.lis
lronaccal from=\$1.cub  to=\$1.lvl1.cub -batchlist=nac.lis
rm *E.cub
lronacecho from=\$1.lvl1.cub to=\$1.lvl2.cub -batchlist=nac.lis
rm *.lvl1.cub
cam2map from=\$1.lvl2.cub to=\$1.map.cub map=./projection.map matchmap=no pixres=CAMERA defaultrange=MINIMIZE -batchlist=nac.lis
rm *.lvl2.cub
stretch from=\$1.map.cub to=\$1.stretch.cub usepercentages=yes pairs="0.:1 0.5:1 99.5:254 100.:254" -batchlist=nac.lis
rm *.map.cub
cubeatt from=\$1.stretch.cub to=\$1.cubeatt.map.cub+lsb+tile+attached+unsignedbyte+1:254 -batchlist=nac.lis
rm *.stretch.cub

