#!/bin/bash
#
#$BATCH --job-name=bwa_job
#$BATCH -N 1 # number of nodes
#SBATCH -n 1 # TOTAL number of cores/tasks
#SBATCH --partition=nodo.q
#SBATCH --exclusive
#SBATCH --time=15:00


DATA_DIR=/home/master/biom/biom-tutor/Mojavensis/bwa
EXE_DIR=/home/master/biom/biom-tutor/BWA/bwa-0.7.17
hostname
echo $SLURM_NTASKS
echo "Start"
STARTTIME=$(date +%s)
$EXE_DIR/bwa mem -t $SLURM_NTASKS $DATA_DIR/3-DMo.fa $DATA_DIR/3-DMo-R1.fastq $DATA_DIR/3-DMo-R2.fastq > aln_pe-$SLURM_NTASKS.sam
ENDTIME=$(date +%s)
echo "End"
echo "It took $(($ENDTIME - $STARTTIME)) seconds to complete bwa..."