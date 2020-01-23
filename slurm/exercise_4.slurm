#!/bin/bash
#SBATCH --job-name=exercise_4
#SBATCH --output=exercise_4-output
#SBATCH --partition=research.q
#SBATCH --array=0-4

echo $(sort names_$SLURM_ARRAY_TASK_ID.txt) > names_$SLURM_ARRAY_TASK_ID.txt
