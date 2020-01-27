#!/bin/bash
#SBATCH --job-name=mpi_prime      # Job name
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=mpi_prime_%j.out     # Standard output and error log
#SBATCH --partition=research.q
hostname
date

echo "Running prime number generator program on $SLURM_JOB_NUM_NODES nodes with $SLURM_NTASKS tasks, each with $SLURM_CPUS_PER_TASK cores."

source /soft/modules-3.2.10/Modules/3.2.10/init/bash
module load openmpi/3.0.0

mpirun -n $SLURM_NTASKS ./prime_mpi

date

