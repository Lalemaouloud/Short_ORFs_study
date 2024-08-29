import pandas as pd
import os

base_dir = 'test_kmer_31'

def process_abundance_file(file_path):
    try:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(file_path, sep='\t')

        # Check if the expected 'tpm' column is present
        if 'tpm' not in df.columns or 'target_id' not in df.columns:
            print(f"File {file_path} does not contain required columns. Skipping.")
            return

        # Extract TPM values and gene IDs
        tpm_values = df['tpm']
        gene_ids = df['target_id']

        # Create lists for gene IDs based on TPM values
        genes_with_zero_tpm = gene_ids[tpm_values == 0].tolist()
        genes_with_nonzero_tpm = gene_ids[tpm_values > 0].tolist()

        # Create output file paths
        dir_path = os.path.dirname(file_path)
        zero_tpm_file = os.path.join(dir_path, 'genes_with_zero_tpm.txt')
        nonzero_tpm_file = os.path.join(dir_path, 'genes_with_nonzero_tpm.txt')

        # Write gene IDs with TPM = 0 to a file
        with open(zero_tpm_file, 'w') as zero_file:
            for gene_id in genes_with_zero_tpm:
                zero_file.write(f"{gene_id}\n")

        # Write gene IDs with TPM > 0 to a file
        with open(nonzero_tpm_file, 'w') as nonzero_file:
            for gene_id in genes_with_nonzero_tpm:
                nonzero_file.write(f"{gene_id}\n")

        print(f"Processed file {file_path} successfully.")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main(base_directory):
    # Walk through all directories and files
    for root, dirs, files in os.walk(base_directory):
        if 'abundance.tsv' in files:
            file_path = os.path.join(root, 'abundance.tsv')
            process_abundance_file(file_path)

if __name__ == '__main__':
    main(base_dir)

