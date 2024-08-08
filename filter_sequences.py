#This script reads the gene_calls.faa ggCaller's output file, filters out genes sequences that are longuer than 100 bp (short ORFs), and writes the remaining sequences to a new file
#Author : LM

def filter_short_sequences(input_file, output_file, max_length):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        write_sequence = False
        current_sequence = ""
        header = ""

        for line in infile:
            if line.startswith(">"):
                if write_sequence and len(current_sequence) <= max_length:
                    outfile.write(header + current_sequence + "\n")
                header = line
                current_sequence = ""
                write_sequence = True
            else:
                current_sequence += line.strip()

        # Check last sequence
        if write_sequence and len(current_sequence) <= max_length:
            outfile.write(header + current_sequence + "\n")

# Exemple d'utilisation (nom des files) :
input_file = "gene_calls.faa"
output_file = "short_orfs.faa"
max_length = 100

filter_short_sequences(input_file, output_file, max_length)
