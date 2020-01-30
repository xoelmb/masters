#!/bin/bash
#SBATCH --job-name=container
#SBATCH --output=container.output
#SBATCH --partition=research.q
#SBATCH --nodes=1
#SBATCH --nodelist=aolin23
module load singularity/3.0.2

cat text1.txt | singularity exec first_container.sif cowsay | singularity exec first_container.sif lolcat

