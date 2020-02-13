#!/bin/bash

jid1=$(sbatch --partition=research.q job1.slurm | cut -f 4 -d' ')

jid2=$(sbatch --partition=research.q job2.slurm | cut -f 4 -d' ')

jid3=$(sbatch --partition=research.q --dependency=afterok:$jid1 job3.slurm | cut -f 4 -d' ')

jid4=$(sbatch --partition=research.q --dependency=afterok:$jid2 job4.slurm | cut -f 4 -d' ')

jid5=$(sbatch --partition=research.q --dependency=afterok:$jid1:$jid2 job5.slurm | cut -f 4 -d' ')

jid6=$(sbatch --partition=research.q --dependency=afterok:$jid3:$jid4 job6.slurm | cut -f 4 -d' ')

jid7=$(sbatch --partition=research.q --dependency=afterok:$jid4:$jid5 job7.slurm | cut -f 4 -d' ')

jid8=$(sbatch --partition=research.q --dependency=afterok:$jid6:$jid7 job8.slurm | cut -f 4 -d' ')