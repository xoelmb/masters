#!/bin/python

from datetime import datetime
import subprocess
print("Start dependent job at", datetime.today())

# first job - no dependencies

print(datetime.today())

jid1 = subprocess.run("sbatch --partition=research.q job1.slurm | cut -f 4 -d' '".split(" "), capture_output=)

jid1=$(sbatch --partition=research.q job1.slurm | cut -f 4 -d' ')

echo $jid1

# multiple jobs can depend on a single job
jid2=$(sbatch  --partition=research.q --dependency=afterok:$jid1 job2.slurm | cut -f 4 -d' ')
jid3=$(sbatch  --partition=research.q --dependency=afterok:$jid1 job3.slurm | cut -f 4 -d' ')

# a single job can depend on multiple jobs
jid4=$(sbatch  --partition=research.q --dependency=afterany:$jid2:$jid3 job4.slurm | cut -f 4 -d' ')

jid5=$(sbatch --partition=research.q --dependency=afterany:$jid4 job5.slurm | cut -f 4 -d' ')

# show dependencies in squeue output:
squeue -u $USER -o "%.8A %.4C %.10m %.20E"

# print final date and time
echo "End dependent job at $(date)"
