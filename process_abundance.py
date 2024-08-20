import pandas as pd
#input.txt a file containing all the paths to our kallisto's abundance.tsv outputs : run in the folder : ls -d -1 $PWD/*.tsv > input.txt
def process_abundance_file(file_path, gene_status):
    """Process a single abundance file and update the gene_status dictionary."""
    try:
        # Read the abundance.tsv file into a DataFrame
        df = pd.read_csv(file_path, sep='\t')
        
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            gene_id = row['target_id']
            tpm = row['tpm']
            
            # Update the status if TPM > 11 ref : https: //www.ebi.ac.uk/gxa/FAQ.html#:~:text=Light%20blue%20box%3A%20expression%20level,or%20more%20than%201000%20TPM)

            if tpm > 11:
                gene_status[gene_id] = True
    
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main():
    # Dictionary to store gene IDs and their statuses
    gene_status = {}
    #print(gene_status)
    try:
        with open('input.txt', 'r') as file:
            paths = file.readlines()
        for path in paths:
            path = path.strip()
            if path:
                process_abundance_file(path, gene_status)
    
    except FileNotFoundError:
        print("input.txt not found. Please make sure the file exists")
    except Exception as e:
        print(f"Error reading input.txt: {e}")
    
    # Print the final gene_status dictionary
    for gene_id, status in gene_status.items():
        print(f"{gene_id}: {'TRUE' if status else 'FALSE'}")

if __name__ == "__main__":
    main()

