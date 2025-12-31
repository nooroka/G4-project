#!/bin/bash

# Path to the genome FASTA file
GENOME_FASTA="../../hg19_new.fna"

# Directory containing  FASTA files
FASTA_DIR="/data/nooroka/grant/punkt1/stage2/cleaned_fasta"

# Output directory
OUTPUT_DIR=" /data/nooroka/grant/punkt1/stage2/cleaned_gc"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Loop over each BED file in the directory
for FASTA_FILE in $FASTA_DIR/*.fasta; do
    # Get the base name of the FASTA file (without extension)
    BASE_NAME=$(basename $FASTA_FILE .fasta)
    
    # Define the output file name
    OUTPUT_FILE="${OUTPUT_DIR}/${BASE_NAME}.geecee"
    
    # Run bedtools getfasta
    geecee $FASTA_FILE  $OUTPUT_FILE
    
    echo "Extracted sequences from $FASTA_FILE to $OUTPUT_FILE"
done
