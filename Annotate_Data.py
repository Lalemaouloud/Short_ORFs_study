import os

def update_gene_status(gene_status_dict, gene_id, tpm_value):
    if gene_id in gene_status_dict:
        if tpm_value != 0:
            gene_status_dict[gene_id] = 1
    else:
        gene_status_dict[gene_id] = 1 if tpm_value != 0 else 0

def process_abundance_files(directory_path, num_files=2):
    gene_status_dict = {}

    for i in range(1, num_files + 1):
        file_path = os.path.join(directory_path, f"abundance_{i}.tsv")
        
 
        with open(file_path, 'r') as file:

            next(file)
            for line in file:

                columns = line.strip().split("\t")
                gene_id = columns[0]
                tpm = float(columns[4])

                update_gene_status(gene_status_dict, gene_id, tpm)

    return gene_status_dict
 
directory_path = "/Users/maouloudlale/Desktop/abundances"
gene_status_dict = process_abundance_files(directory_path)


#for gene_id, status in gene_status_dict.items():
 #   print(f"Gene: {gene_id}, Status: {status}")
#print(gene_status_dict)




##Part 2



def parse_fasta_and_add_status(fasta_file, gene_status_dict, output_file):
    with open(fasta_file, 'r') as f_in, open(output_file, 'w') as f_out:
        gene_id = None
        sequence = []
        
        for line in f_in:
            if line.startswith(">"):
 
                if gene_id:
 
                    status = gene_status_dict.get(gene_id, 0)
                    f_out.write(f"{header}\n{''.join(sequence)}\n{status}\n")
                
 
                header = line.strip()
                gene_id = header.split()[0][1:]
                sequence = []
            else:

                sequence.append(line.strip())

        if gene_id:
            status = gene_status_dict.get(gene_id, 0)
            f_out.write(f"{header}\n{''.join(sequence)}\n{status}\n")

fasta_file = "short_orfs.ffn"
output_file = "labeled_data_orfs.ffn"
parse_fasta_and_add_status(fasta_file, gene_status_dict, output_file)

print("Done! :)", output_file)
