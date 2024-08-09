import os
import subprocess
from Bio import SeqIO

# input files
filtered_gene_calls_faa = "short_orfs.faa"
all_transcripts_fasta = "/nfs/research/jlees/lale/small_ORFs/data/RNA-seq_data/SRA_FILES_Complete/sra_fasta_files/All_transcripts.fasta"

# Output files
true_genes_fasta = "True_genes.fasta"
false_genes_fasta = "False_genes.fasta"

# Bowtie2 index basename
transcripts_index_basename = "transcripts_index"

# Bowtie2 alignment output
alignment_output = "alignment_output.sam"

# Percentage match threshold
match_threshold = 0.95

def build_bowtie2_index(fasta_file, index_basename):
    """Build Bowtie2 index for the transcript file."""
    subprocess.run(["bowtie2-build", fasta_file, index_basename], check=True)

def align_with_bowtie2(index_basename, fasta_file, output_sam):
    """Align sequences using Bowtie2."""
    command = [
        "bowtie2",
        "-x", index_basename,
        "-f", fasta_file,
        "-S", output_sam,
        "--very-sensitive",
        "--no-unal"  # Do not write unaligned reads to the SAM output
    ]
    subprocess.run(command, check=True)

def parse_alignment_results(sam_file, gene_sequences):
    """Parse SAM file to determine TRUE and FALSE genes."""
    true_genes = set()
    false_genes = set(gene_sequences.keys())

    with open(sam_file, 'r') as sam:
        for line in sam:
            if line.startswith("@"):  # Skip header lines
                continue
            fields = line.split("\t")
            gene_id = fields[0]
            flag = int(fields[1])
            cigar = fields[5]

            if "M" in cigar:
                match_count = sum(int(num) for num in cigar.split("M")[0].split("I"))
                gene_len = len(gene_sequences[gene_id])
                match_ratio = match_count / gene_len

                if match_ratio >= match_threshold:
                    true_genes.add(gene_id)
                    false_genes.discard(gene_id)

    return true_genes, false_genes

def write_fasta(sequences, output_file):
    """Write sequences to a FASTA file."""
    with open(output_file, 'w') as out_fasta:
        SeqIO.write(sequences, out_fasta, 'fasta')
from Bio import SeqIO

def load_unique_sequences(fasta_file):
    """Load sequences from a FASTA file into a dictionary, skipping duplicates."""
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        if record.id in sequences:
            print(f"Warning: Duplicate key '{record.id}' found. Skipping...")
            continue
        sequences[record.id] = record
    return sequences

def main():
    # Step 1: Build Bowtie2 index for all_transcripts.fasta
    build_bowtie2_index(all_transcripts_fasta, transcripts_index_basename)

    # Step 2: Align filtered_gene_calls.faa to the transcripts index
    align_with_bowtie2(transcripts_index_basename, filtered_gene_calls_faa, alignment_output)

    # Step 3: Parse alignment results and classify genes
    gene_sequences = load_unique_sequences(filtered_gene_calls_faa)  # Use the new function to load sequences
    true_genes, false_genes = parse_alignment_results(alignment_output, gene_sequences)

    # Step 4: Write TRUE and FALSE genes to separate files
    write_fasta([gene_sequences[gid] for gid in true_genes], true_genes_fasta)
    write_fasta([gene_sequences[gid] for gid in false_genes], false_genes_fasta)

if __name__ == "__main__":
    main()

