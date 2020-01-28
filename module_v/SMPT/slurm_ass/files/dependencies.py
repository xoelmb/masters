#!/bin/python

from datetime import datetime
import subprocess

print("Start dependent job at", datetime.today())

# first job - no dependencies

print(datetime.today())

jid1 = str(subprocess.check_output("sbatch --partition=research.q job1.files".split()))
jid1 = ''.join([c for c in jid1 if c.isnumeric()])
print(jid1)

# multiple jobs can depend on a single job
jid2 = str(subprocess.check_output(f"sbatch  --partition=research.q --dependency=afterok:{jid1} job2.files".split()))
jid2 = ''.join([c for c in jid2 if c.isnumeric()])
jid3 = str(subprocess.check_output(f"sbatch  --partition=research.q --dependency=afterok:{jid1} job3.files".split()))
jid3 = ''.join([c for c in jid3 if c.isnumeric()])

# a single job can depend on multiple jobs
jid4 = str(subprocess.check_output(f"sbatch  --partition=research.q --dependency=afterany:{jid2}:{jid3} job4.files".split()))
jid4 = ''.join([c for c in jid4 if c.isnumeric()])
jid5 = str(subprocess.check_output(f"sbatch --partition=research.q --dependency=afterany:{jid4} job5.files".split()))
jid5 = ''.join([c for c in jid5 if c.isnumeric()])

# show dependencies in squeue output:
user = subprocess.check_output(['whoami']).decode('utf-8').strip()
format_op = '"%.8A %.4C %.10m %.20E"'
command = 'squeue -u ' + user + ' -o '
command = command.split()
command.append(format_op)
print(subprocess.check_output(command).decode('utf-8').replace('"', ''))

# # print final date and time
print(f"End dependent job at {datetime.today()}")
