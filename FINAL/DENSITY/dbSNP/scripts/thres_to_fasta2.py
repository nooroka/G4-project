#!/usr/bin/env python3
import pandas as pd
import sys
file_path = sys.argv[1]

if file_path == '-':
    data = pd.read_csv(sys.stdin, sep='\t', header=None)
else:
    data = pd.read_csv(file_path, sep='\t', header=None)
filtered_data = data[[0, 3]]

fasta_file_path = sys.argv[2]

with open(fasta_file_path, 'w') as fasta_file:
    for i, seq in enumerate(filtered_data[3], start=1):
        fasta_file.write(f">{i}\n{seq}\n")
