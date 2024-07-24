#Script to download the SRR data in FASTA format for a specified BioProject, in our case "PRJNA422256"
#Note : First, make sure you have the SRA Toolkit installed. If not, you can download it from : https://github.com/ncbi/sra-tools/wiki/
#Author : Lale MAOULOUD 
import os

#The List of SRR accessions from the RNA-seq study
srr_accessions = [
    "SRR6372904", "SRR6372905", "SRR6372906", "SRR6372907", "SRR6372908",
    "SRR6372909", "SRR6372910", "SRR6372911", "SRR6372912", "SRR6372913",
    "SRR6372914", "SRR6372915", "SRR6372916", "SRR6372917", "SRR6372918",
    "SRR6372919", "SRR6372920", "SRR6372921", "SRR6372922", "SRR6372923",
    "SRR6372924", "SRR6372925", "SRR6372926", "SRR6372927", "SRR6372928",
    "SRR6372929", "SRR6372930", "SRR6372931", "SRR6372932", "SRR6372933",
    "SRR6372934", "SRR6372935", "SRR6372936", "SRR6372937"
]


output_dir = "sra_fasta_files"
os.makedirs(output_dir, exist_ok=True)

# to download SRR data in FASTA format
def download_srr_fasta(srr_id, output_dir):
    fasta_file = os.path.join(output_dir, f"{srr_id}.fasta")
    os.system(f"fastq-dump --fasta 0 {srr_id} -O {output_dir}")

# Loop & download the data
for srr in srr_accessions:
    download_srr_fasta(srr, output_dir)

print("Download completed.")
