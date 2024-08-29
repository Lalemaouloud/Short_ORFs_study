# Small ORF Expression Prediction Model

## Overview

This project aims to develop a machine learning model to predict the expression of small Open Reading Frames (sORFs). Small ORFs are typically challenging to identify and predict due to their short length, but they play a significant role in various biological processes. By accurately predicting which sORFs are expressed, we can gain insights into their functional roles in the genome.

## Project Workflow

### 1. Gene Identification with ggCaller

The initial step in the project involved identifying potential small ORFs from a dataset of **616 pneumococcal genomes** sourced from [Bentley et al. 2015](https://www.nature.com/articles/sdata201558). The following steps were performed:

- **Tool Used:** [ggCaller](https://github.com/ghoresh11/ggCaller)
- **Parameters:**
  - `--min-orf-length` = 19
  - `--min-orf-score` = 19

The ggCaller tool was used to predict small ORFs from these genomes. After running ggCaller, a total of **6,013 genes** were predicted.

Here is the distribution of the genes after filtering the long ORFs:

![Gene Distribution](path_to_figure)

### 2. Transcript Alignment with Kallisto

The next step was to align the transcripts from the study [Delcher et al. 2018](https://pubmed.ncbi.nlm.nih.gov/30165663/) to the identified small ORFs to determine which of these ORFs are expressed.

- **Tool Used:** [Kallisto](https://pachterlab.github.io/kallisto/about)
- **Index File:** `short_ORFs.ffn`
- **Parameters:**
  - `kmer length` = 19

The alignment was performed using the cDNA expression data from the study. The dataset was accessed from the [European Nucleotide Archive (ENA)](https://www.ebi.ac.uk/ena/browser/view/PRJNA422256?show=reads).

### 3. Kallisto Output Analysis

After the alignment, the output from Kallisto was analyzed, specifically focusing on the `abundance.tsv` file. The key metrics in this file are:

- **eff_length:** The effective length of the transcript, considering the fragment length distribution.
- **est_counts:** The estimated number of reads derived from this transcript.
- **TPM (Transcripts Per Million):** A normalized measure of transcript abundance, allowing comparison of transcript levels within and between samples.

#### TPM Calculation:

1. **RPK (Reads Per Kilobase):** Divide the read counts by the length of each gene in kilobases.
2. **Per Million Scaling Factor:** Count up all the RPK values in a sample and divide by 1,000,000.
3. **TPM:** Divide the RPK values by the “per million” scaling factor.

**Note:** TPM is preferred over RPKM/FPKM because it ensures that the sum of TPMs in each sample is the same, making cross-sample comparisons more reliable.

Here is an example distribution of TPM values:

![TPM Distribution](path_to_figure)

### 4. Labeling Genes for Model Training

To determine whether a gene is expressed (True) or not (False), a TPM cutoff of **0** was used.

- **True Genes:** Genes with a TPM > 0.
- **False Genes:** Genes with a TPM = 0.

The following steps were taken:

- Gene IDs were read from `genes_with_zero_tpm.txt` and `genes_with_nonzero_tpm.txt` files.
- The `short_orfs.ffn` file was parsed, and each gene's sequence was modified based on its TPM status.
- The output was a modified `short_orfs.ffn` file with `0` (False) or `1` (True) appended under each gene's sequence.

### 5. Final Training File

The final training file, which will be used to train the machine learning model, looks something like this:

```plaintext
>gene_1
ATGCGT...TTGA
0

>gene_2
ATGCCA...TCAA
1
