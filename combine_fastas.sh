#!/bin/bash
#SBATCH -t 98:00:00               # Time limit 
#SBATCH --mem=80G                # Memory 
#SBATCH -o Run_out.txt            # Standard output file
#SBATCH -e Run_err.txt            # Standard error file
#SBATCH --mail-user=lale@ebi.ac.uk # Email for notifications
#SBATCH --cpus-per-task=40        # Number of CPU cores
#SBATCH --mail-type=BEGIN         # Email when the job starts
#SBATCH --mail-type=END           # Email when the job ends


#SLURM bash script that combine all .fasta files in the directory into one file named All_transcripts.fasta
# to execute run : sbatch combine_fastas.sh

#Author : LM



cd /nfs/research/jlees/lale/small_ORFs/data/RNA-seq_data/SRA_FILES_Complete/sra_fasta_files

# Define the output file
output_file="All_transcripts.fasta"

# Remove the output file if it already exists
if [ -f "$output_file" ]; then
    rm "$output_file"
fi

# Iterate over all .fasta files and append their content to the output file
for file in *.fasta; do
    if [ -f "$file" ]; then
        cat "$file" >> "$output_file"
        echo "" >> "$output_file"  # Add a newline for separation
    fi
done

echo "All transcripts have been combined into $output_file"




#To make sure the script worked you can run : grep -c ">" *.fasta | awk '{sum += $1} END {print sum}' which will give you the number of ">" characters across all .fasta files
# and then run grep -c ">" All_transcripts.fasta | awk '{sum += $1} END {print sum} to know also the number of sequences in the combined file. 

