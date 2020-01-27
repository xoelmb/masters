#!/bin/bash
#SBATCH --job-name=exercise_8
#SBATCH --output=exercise_8-output
#SBATCH --partition=research.q
#SBATCH --nodelist=aolin23,aolin24
#SBATCH --exclusive

perf stat bash bwa_example.sh
echo -e "1\n2\n3\n4\n5\n6\n7\n8" | perf stat xargs -n1 -P8 -I{} /usr/bin/bwa index example{}.fastq
rm example*.fastq.*