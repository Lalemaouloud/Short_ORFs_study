#!/bin/bash

if [ ! -f "abundance.tsv" ]; then
    echo "File abundance.tsv not found!"
    exit 1
fi

# Extracting the tpm colonne 
awk 'NR>1 {print $5}' abundance.tsv | sort -n | uniq -c | awk '{print "TPM: " $2 ", Count: " $1}'


## this script gives the distribution of tpm values in the abundance.tsv file (output of kallisto), showing each unique tpm value along with the number of occurrences (frequence).
