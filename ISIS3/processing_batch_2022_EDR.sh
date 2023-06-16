#!/bin/sh
source /cluster/projects/nn8026k/miniconda3/etc/profile.d/conda.sh
conda activate isis
echo $CONDA_DEFAULT_ENV

# This version of the script process all the image at the same time (i.e., conducting the first for all images
# and then so forth until the end). This is nice
ls -1 *E.IMG | cut -d. -f1 > nac.lis

lronac2isis from=\$1.IMG to=\$1.cub -batchlist=nac.lis
spiceinit from=\$1.cub -batchlist=nac.lis
lronaccal from=\$1.cub  to=\$1.lvl1.cub -batchlist=nac.lis
lronacecho from=\$1.lvl1.cub to=\$1.lvl2.cub -batchlist=nac.lis
cam2map from=\$1.lvl2.cub to=\$1.map.cub map=./projection.map matchmap=no pixres=CAMERA defaultrange=MINIMIZE -batchlist=nac.lis
stretch from=\$1.map.cub to=\$1.stretch.cub usepercentages=yes pairs="0.:1 100.:254" -batchlist=nac.lis
cubeatt from=\$1.stretch.cub to=\$1.cubeatt.map.cub+lsb+tile+attached+unsignedbyte+1:254 -batchlist=nac.lis