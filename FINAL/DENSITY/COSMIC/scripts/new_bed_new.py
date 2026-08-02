import pandas as pd
import sys

# Путь к файлу
file_path = 'Cosmic_NonCodingVariants_v102_GRCh37.tsv.gz'

# Считываем файл сразу из gz
cols = ['CHROMOSOME', 'GENOME_START', 'GENOME_STOP','HGVSG']
df = pd.read_csv(file_path, sep='\t', compression='gzip', usecols=cols,  dtype={10: str})

# Фильтруем по хромосоме 13
df_chr13 = df[df['CHROMOSOME'] == str(sys.argv[1])].copy()  
df_chr13.drop_duplicates(subset=['HGVSG'], inplace=True)
# Сдвигаем START на -1
df_chr13['GENOME_START'] = df_chr13['GENOME_START'] - 1  
df_chr13['CHROMOSOME'] = 'chr' + df_chr13['CHROMOSOME'].astype(str)
# Сохраняем результат
df_chr13.to_csv(f'chr{sys.argv[1]}_coordinates_shifted_tab_hgvsg_new.bed', index=False,sep="\t")

#print(f"Количество мутаций на хромосоме 13: {len(df_chr13)}")
#print(df_chr13.head())
