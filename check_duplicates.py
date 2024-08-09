from Bio import SeqIO
from collections import Counter

def find_duplicates(fasta_file):
    """Find and print duplicate sequence identifiers in a FASTA file."""
    ids = [record.id for record in SeqIO.parse(fasta_file, "fasta")]
    duplicates = [item for item, count in Counter(ids).items() if count > 1]
    if duplicates:
        print("Duplicate identifiers found:")
        for dup in duplicates:
            print(dup)
    else:
        print("No duplicates found.")
 
filtered_gene_calls_faa = "filtered_gene_calls.faa"
find_duplicates(filtered_gene_calls_faa)
