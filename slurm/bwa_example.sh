#!/bin/bash
/usr/bin/bwa index sample1.fastq &
/usr/bin/bwa index sample2.fastq &
/usr/bin/bwa index sample3.fastq &
wait
echo "All processes completed"