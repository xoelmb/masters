#!/bin/bash
#SBATCH --job-name=array-job
#SBATCH --open-mode=append
#SBATCH --partition=research.q
#SBATCH --array=1-24
#SBATCH --nodes=1-3

# print initial date and time
echo "Start at $(date)"
echo "-------------------------"
# print name of host
hostname
echo "-------------------------"

# sleep 20 seconds 
sleep 20

# print final date and time
echo "End at $(date)"
exit 0

