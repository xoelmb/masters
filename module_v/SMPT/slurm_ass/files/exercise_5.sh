#!/bin/bash

# print initial date and time
echo "Start dependentjob at $(date)"
dia=$(date)
echo $dia

# first job - no dependencies
jid1=$(sbatch --partition=research.q job1.files | cut -f 4 -d' ')
echo $jid1

# multiple jobs can depend on a single job
jid2=$(sbatch --partition=research.q --dependency=afterok:$jid1 job2.files | cut -f 4 -d' ')
jid3=$(sbatch --partition=research.q --dependency=afterok:$jid1 job3.files | cut -f 4 -d' ')

# a single job can depend on multiple jobs
jid4=$(sbatch --partition=research.q --dependency=afterany:$jid2:$jid3 job4.files | cut -f 4 -d' ')
jid5=$(sbatch --partition=research.q --dependency=afterany:$jid4 job5.files | cut -f 4 -d' ')

# show dependencies in squeue output:
squeue -u $USER -o "%.8A %.4C %.10m %.20E"

# print final date and time
echo "End dependent job at $(date)"
