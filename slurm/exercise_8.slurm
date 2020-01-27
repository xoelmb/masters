#!/bin/bash
#SBATCH --job-name=exercise_8
#SBATCH --output=exercise_8-output
#SBATCH --partition=research.q
#SBATCH --nodelist=aolin23,aolin24
#SBATCH --exclusive

perf stat bash bwa_example.sh