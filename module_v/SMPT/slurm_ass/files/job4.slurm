#!/bin/bash
#SBATCH --job-name=basic-job
#SBATCH --output=basic-job4-output
#SBATCH --partition=research.q
#SBATCH --nodelist=aolin23,aolin24

# print initial date and time
echo "Start JOB 4 at $(date)"
echo "-------------------------"
# print name of host
hostname
echo "-------------------------"

# sleep 20 seconds 
sleep 20

# print initial date and time
echo "End JOB 4 at $(date)"

