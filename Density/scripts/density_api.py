import os
import gzip
from collections import defaultdict
import pandas as pd
import numpy as np
import requests

def download_dbsnp_current():
    base_url = "https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/"
    files = [
        "GCF_000001405.25.gz",       # Основной файл (build 25)
        "GCF_000001405.25.gz.tbi",   # Индекс
        "GCF_000001405.40.gz",       # Альтернативная версия (build 40)
        "GCF_000001405.40.gz.tbi"    # Индекс
    ]
    
    for file in files:
        print(f"Скачиваю {file}...")
        try:
            response = requests.get(base_url + file, stream=True)
            response.raise_for_status()
            
            with open(file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Успешно скачан {file}")
        except Exception as e:
            print(f"Ошибка при скачивании {file}: {str(e)}")

download_dbsnp_current()


import gzip
import pandas as pd

def extract_chromosomes():
    input_file = "GCF_000001405.40.gz"  # Используем актуальную версию
    output_dir = "by_chromosome"
    
    os.makedirs(output_dir, exist_ok=True)
    
    chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y']
    writers = {chrom: open(f"{output_dir}/chr{chrom}.vcf", 'w') for chrom in chromosomes}
    
    with gzip.open(input_file, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                # Записываем заголовки во все файлы
                for writer in writers.values():
                    writer.write(line)
            else:
                chrom = line.split('\t')[0]
                if chrom in writers:
                    writers[chrom].write(line)
    
    for writer in writers.values():
        writer.close()

extract_chromosomes()


def process_all_chromosomes():
    chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y']
    results = []
    
    for chrom in chromosomes:
        input_file = f"by_chromosome/chr{chrom}.vcf"
        if not os.path.exists(input_file):
            continue
        print(input_file)    
        df = pd.read_csv(input_file, sep='\t', comment='#',
                        usecols=['#CHROM', 'POS'],
                        dtype={'#CHROM': str, 'POS': int})
        print(df)
        
        # Расчёт плотности (пример для хромосомы 1)
        density = len(df) / (250e6 / 1e6)  # Примерная длина / 1 Мб
        
        results.append({
            'chromosome': chrom,
            'snp_count': len(df),
            'density_per_mb': density
        })
    
    pd.DataFrame(results).to_csv("chromosome_density.csv", index=False)

process_all_chromosomes()

