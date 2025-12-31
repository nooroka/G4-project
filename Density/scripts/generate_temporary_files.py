#!/usr/bin/env python3
import gzip
import os
from collections import defaultdict
from pathlib import Path
import concurrent.futures
import bisect

def process_chromosome(args):
    """Обработка одной хромосомы с обработкой исключений"""
    chr, quad_bed, dbsnp_dir = args
    chr_str = f"chr{chr}"
    
    try:
        # 1. Загрузка квадруплексов
        quad_intervals = []
        with open(quad_bed) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3 and parts[0] == chr_str:
                    try:
                        start, end = int(parts[1]), int(parts[2])
                        quad_intervals.append((start, end))
                    except (ValueError, IndexError):
                        continue

        if not quad_intervals:
            print(f"No quadruplexes found for {chr_str}")
            return None

        # 2. Загрузка SNP
        snp_positions = []
        vcf_file = Path(dbsnp_dir) / f"chr{chr}.vcf.gz"
        try:
            with gzip.open(vcf_file, 'rt') as f:
                for line in f:
                    if not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 2:
                            try:
                                pos = int(parts[1])
                                snp_positions.append(pos)
                            except (ValueError, IndexError):
                                continue
        except Exception as e:
            print(f"Error reading {vcf_file}: {str(e)}")
            return None

        # 3. Поиск пересечений
        snp_positions.sort()
        quad_counts = defaultdict(int)

        for start, end in quad_intervals:
            left = bisect.bisect_left(snp_positions, start + 1)
            right = bisect.bisect_right(snp_positions, end)
            count = right - left
            if count > 0:
                quad_counts[(start, end)] = count

        # 4. Расчет статистик
        total_len = sum(end - start for start, end in quad_intervals)
        total_snp = sum(quad_counts.values())
        density = total_snp / (total_len / 1000) if total_len > 0 else 0

        return {
            'chromosome': chr_str,
            'total_len': total_len,
            'total_snp': total_snp,
            'density': density
        }

    except Exception as e:
        print(f"Error processing {chr_str}: {str(e)}")
        return None

def main():
    # Конфигурация
    QUAD_BED = "/data/nooroka/grant/punkt1/stage2/sorted/quadr7_chain180424_merged2_sorted_39_copy.bed"
    DBSNP_DIR = "/mnt/work/nooroka/dbSNP_chromosomes"
    OUTPUT_FILE = "dbsnp_density_per_chrom_39.txt"
    CHROMOSOMES = list(range(1, 23)) + ['X', 'Y']
    MAX_WORKERS = min(4, len(CHROMOSOMES))  # Ограничиваем число процессов

    # Проверка файлов
    if not os.path.exists(QUAD_BED):
        print(f"Quadruplex file not found: {QUAD_BED}")
        return
    if not os.path.exists(DBSNP_DIR):
        print(f"dbSNP directory not found: {DBSNP_DIR}")
        return

    # Подготовка аргументов
    args_list = [(chr, QUAD_BED, DBSNP_DIR) for chr in CHROMOSOMES]

    # Заголовок выходного файла
    with open(OUTPUT_FILE, 'w') as out:
        out.write("Chromosome\tQuadLength(bp)\tSNP_count\tDensity(SNP/kb)\n")

    # Обработка с ограничением числа попыток
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
                for result in executor.map(process_chromosome, args_list):
                    if result:
                        with open(OUTPUT_FILE, 'a') as out:
                            out.write(f"{result['chromosome']}\t{result['total_len']}\t{result['total_snp']}\t{result['density']:.2f}\n")
            break  # Успешное завершение
        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts} failed: {str(e)}")
            if attempts == max_attempts:
                print("Max attempts reached, falling back to sequential processing")
                # Последовательная обработка при неудаче
                for args in args_list:
                    result = process_chromosome(args)
                    if result:
                        with open(OUTPUT_FILE, 'a') as out:
                            out.write(f"{result['chromosome']}\t{result['total_len']}\t{result['total_snp']}\t{result['density']:.2f}\n")
                break

    print("Processing completed")

if __name__ == "__main__":
    main()
