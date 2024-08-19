#!/bin/bash

index="short_orfs.index"

fragment_length=75
std_dev=10


for file in *.fastq.gz; do
    # extract the base name of the file - remove the .fastq.gz extension
    base=$(basename $file .fastq.gz)

    # an output directory for each file
    output_dir="${base}_kallisto_output"
    mkdir -p $output_dir

    # Run Kallisto command
    kallisto quant -i $index -o $output_dir --single -l $fragment_length -s $std_dev $file

    echo "Finished processing $file"
done
