#!/usr/bin/env python3
import pandas as pd
import sys

# Чтение данных из файла или stdin
file_path = sys.argv[1]

if file_path == '-':
    # Читаем из stdin
    data = pd.read_csv(sys.stdin, sep='\t', header=None)
else:
    # Читаем из файла
    data = pd.read_csv(file_path, sep='\t', header=None)

# Фильтрация первой и четвертой колонок
filtered_data = data[[0, 3]]

# Создание multiple FASTA file
fasta_file_path = sys.argv[2]

#with open(fasta_file_path, 'w') as fasta_file:
 #   for index, row in filtered_data.iterrows():
 #       fasta_file.write(f">{index + 1}\n{row[3]}\n")
with open(fasta_file_path, 'w') as fasta_file:
    for i, seq in enumerate(filtered_data[3], start=1):
        fasta_file.write(f">{i}\n{seq}\n")
