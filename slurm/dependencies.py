#!/bin/python

from datetime import datetime
import subprocess
print("Start dependent job at", datetime.today())

# first job - no dependencies

print(datetime.today())

jid1 = str(subprocess.check_output("sbatch --partition=research.q job1.slurm".split()))
jid1 = ''.join([c for c in jid1 if c.isnumeric()])
print(jid1)

# multiple jobs can depend on a single job
jid2 = str(subprocess.check_output(f"sbatch  --partition=research.q --dependency=afterok:{jid1} job2.slurm".split()))
jid2 = ''.join([c for c in jid2 if c.isnumeric()])
jid3 = str(subprocess.check_output(f"sbatch  --partition=research.q --dependency=afterok:{jid1} job3.slurm".split()))
jid3 = ''.join([c for c in jid3 if c.isnumeric()])

# a single job can depend on multiple jobs
jid4 = str(subprocess.check_output(f"sbatch  --partition=research.q --dependency=afterany:{jid2}:{jid3} job4.slurm".split()))
jid4 = ''.join([c for c in jid4 if c.isnumeric()])
jid5 = str(subprocess.check_output(f"sbatch --partition=research.q --dependency=afterany:{jid4} job5.slurm".split()))
jid5 = ''.join([c for c in jid5 if c.isnumeric()])

# show dependencies in squeue output:
user = str(subprocess.check_output(['whoami']))[2:-3]
format_op = '"%.8A %.4C %.10m %.20E"'
command = f'squeue -u {user} -o '.split()
command = command.append(format_op)
print(command)
print(subprocess.check_output(command).output)

# # print final date and time
print(f"End dependent job at {datetime.today()}")
