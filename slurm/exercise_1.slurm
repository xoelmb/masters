#!/bin/bash
#SBATCH --job-name=exercise_1
#SBATCH --output=exercise_1-output
#SBATCH --partition=research.q
#SBATCH --nodes=1

# Create and write file
echo "I have written a submit script" > text.txt

# Sleep for 30 secs
sleep 30

# List contents in the folder
ls
