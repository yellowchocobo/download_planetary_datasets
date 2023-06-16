#!/bin/sh
#SBATCH --account=nn9010k
#SBATCH --job-name=ISIS3-Moon-NAC-FRESH14
#SBATCH --time=06:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=4
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --partition=normal

## Set up job environment:
set -o errexit  # Exit the script on any error
set -o nounset  # Treat any unset variables as an error

# do some work (ISIS3)
bash processing_batch.sh