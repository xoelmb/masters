#!/bin/bash
/usr/bin/bwa index example1.fastq &>/dev/null
/usr/bin/bwa index example2.fastq &>/dev/null
/usr/bin/bwa index example3.fastq &>/dev/null
echo "All processes completed"