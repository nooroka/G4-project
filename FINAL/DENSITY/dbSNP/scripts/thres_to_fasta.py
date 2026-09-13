import pandas as pd
import sys
# Чтение данных из файла
file_path = sys.argv[1]
#file_path = '../control/gccoords_percents_8_my_39_subtract_from_all_filtered_loop5.txt'
data = pd.read_csv(file_path, sep='\t', header=None)

# Фильтрация первой и четвертой колонок
filtered_data = data[[0, 3]]

# Создание multiple FASTA file
fasta_file_path = sys.argv[2]
#fasta_file_path = '../control/8_filtered_loop5.fasta'
with open(fasta_file_path, 'w') as fasta_file:
    for index, row in filtered_data.iterrows():
        fasta_file.write(f">{index + 1}\n{row[3]}\n")

#with open(fasta_file_path, 'w') as fasta_file:
  #  for index, row in filtered_data.iterrows():
   #     fasta_file.write(f">{row[0]}\n{row[3]}\n")

#print(f"FASTA file created: {fasta_file_path}")
