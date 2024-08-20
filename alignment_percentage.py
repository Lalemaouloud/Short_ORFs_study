def classify_genes(gene_alignments, total_reads, threshold=0.95):
    true_genes = []
    false_genes = []

    for gene_id, est_count in gene_alignments.items():
        # Calculate the percentage of reads aligned
        percentage_aligned = est_count / total_reads

        if percentage_aligned >= threshold:
            true_genes.append(gene_id)
        else:
            false_genes.append(gene_id)

    return true_genes, false_genes

gene_alignments = {
    "GCA_001145465.2_7622_2_42_genomic_-53145": 3.33333,
    "GCA_001133885.2_7622_2_21_genomic_-44209": 3.33333,
    "GCA_001093685.2_7553_4_14_genomic_-10662": 3.33333,
    "GCA_001135065.2_7622_2_16_genomic_-44855": 0.5,
    "GCA_001301215.2_7553_6_3_genomic_-86775": 0.5,
} # from aboundance.tsv

total_reads = 3.5  # from run_info.json

true_genes, false_genes = classify_genes(gene_alignments, total_reads)


print("true_genes", true_genes,"false_genes", false_genes)
