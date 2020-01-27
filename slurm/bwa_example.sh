#!/bin/bash
/usr/bin/bwa index example1.fastq
/usr/bin/bwa index example2.fastq
/usr/bin/bwa index example3.fastq
rm example*.fastq.*
echo "All processes completed"