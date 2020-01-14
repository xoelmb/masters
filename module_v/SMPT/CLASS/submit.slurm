#!/bin/bash
#SBATCH --job-name=xoel
#SBATCH --nodes=1
#SBATCH --partition=research.q

echo 'I have written a submit script' > text.txt
sleep 30
ls
