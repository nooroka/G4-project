#!/bin/bash

GENOME_FASTA="../../hg19_new.fna"

FASTA_DIR="/data/nooroka/grant/punkt1/stage2/cleaned_fasta"
OUTPUT_DIR=" /data/nooroka/grant/punkt1/stage2/cleaned_gc"
mkdir -p $OUTPUT_DIR

for FASTA_FILE in $FASTA_DIR/*.fasta; do
    BASE_NAME=$(basename $FASTA_FILE .fasta)
    OUTPUT_FILE="${OUTPUT_DIR}/${BASE_NAME}.geecee"
    geecee $FASTA_FILE  $OUTPUT_FILE
    
    echo "Extracted sequences from $FASTA_FILE to $OUTPUT_FILE"
done
