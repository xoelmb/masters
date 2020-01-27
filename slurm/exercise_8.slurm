#!/bin/bash
#SBATCH --job-name=exercise_8
#SBATCH --output=exercise_8-output
#SBATCH --partition=research.q
#SBATCH --nodelist=aolin23,aolin24
#SBATCH --cpus-per-task=8
#SBATCH --exclusive
#SBATCH --ntasks=8

perf stat bash bwa_example.sh
rm example*.fastq.*
echo -e "1\n2\n3\n4\n5\n6\n7\n8" | perf stat xargs -n1 -P0 -I{} /usr/bin/bwa index example{}.fastq
rm example*.fastq.*
