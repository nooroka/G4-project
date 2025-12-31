#!/bin/bash

# Path to the genome FASTA file
GENOME_FASTA="/data/nooroka/grant/punkt1/hg19_new.fna"

# Directory containing BED files
BED_DIR="/data/nooroka/grant/punkt3/stage2/gccoords/quadr2"

# Output directory
OUTPUT_DIR="/data/nooroka/grant/punkt1/stage2/cleaned_fasta"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Loop over each BED file in the directory
for BED_FILE in $BED_DIR/*.bed; do
    # Get the base name of the BED file (without extension)
    BASE_NAME=$(basename $BED_FILE .bed)
    
    # Define the output file name
    OUTPUT_FILE="${OUTPUT_DIR}/${BASE_NAME}_cleaned.fasta"
    
    # Run bedtools getfasta
    bedtools getfasta -fi $GENOME_FASTA -bed $BED_FILE -fo $OUTPUT_FILE
    
    echo "Extracted sequences from $BED_FILE to $OUTPUT_FILE"
done
