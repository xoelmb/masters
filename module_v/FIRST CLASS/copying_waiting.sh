#!/bin/bash

input_path = $1
output_path = $2
echo Copying from $input_path to $output_path

i = 1
while [ $i -gt 0 ]
do
scp -r $1 $2 && $i = 0 | echo Done || sleep 1m
done
