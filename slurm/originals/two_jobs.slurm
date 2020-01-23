#!/bin/bash
#SBATCH --job-name=basic-job
#SBATCH	-N 2
#SBATCH -n 2
#SBATCH -c 1
#SBATCH --output=srun-job-output%j.out
#SBATCH --partition=research.q
#SBATCH --nodelist=aolin23,aolin24

# print initial date and time
echo "Start at $(date)"
echo "-------------------------"
# print name of host
hostname

srun -l -N 1 -n 1 job1.sh &
srun -l -N 1 -n 1 job2.sh &

wait
echo "-------------------------"    

# print final date and time
echo "End at $(date)"

