import os
import subprocess

# Пути к файлам
input_dir="/data/nooroka/grant/punkt3/stage2/scripts/temp"
output_file = os.path.join(input_dir, "average_interval_lengths_bed.tsv")
 #Хромосомы для обработки
chromosomes = list(range(1, 23)) + ['X', 'Y']

# Открываем файл для записи результатов
with open(output_file, 'w') as out_f:
    # Записываем заголовок
    out_f.write("Chromosome\tInterval_Count\tTotal_Length\tAverage_Length\n")
    
    for chrom in chromosomes:
        bed_file = os.path.join(input_dir, f"quadr_chr{chrom}.bed")
        count = subprocess.check_output(f'wc -l  temp/merged_intersected_chr{chrom}_bed.bed', shell=True).decode().split()[0]
#
        if not os.path.exists(bed_file):
            print(f"Файл для хромосомы {chrom} не найден, пропускаем")
            continue
        
        total_length = 0
        
        with open(bed_file, 'r') as f:
            for line in f:
                if line.startswith('#') or line.strip() == '':
                    continue  # Пропускаем комментарии и пустые строки
                
                parts = line.strip().split('\t')
                print(parts)
                if len(parts) < 3:
                    continue  # Невалидная строка
                
                try:
                    start = int(parts[1])
                    end = int(parts[2])
                    length = end - start
                    print(start,end,length)
                    total_length += length
                    
                except (ValueError, IndexError):
                    continue  # Пропускаем строки с некорректными данными
        
        # Рассчитываем плотность мутаций
        if int(count) > 0:
            mutation_density   = float(count)/float(total_length)
        else:
            mutation_density = 0.0
        
        # Записываем результаты
        out_f.write(f"chr{chrom}\t{count}\t{total_length}\t{mutation_density:.10f}\n")
        print(f"Обработана хромосома chr{chrom}: интервалов={count}, средняя длина={mutation_density:.10f}")

print(f"Готово! Результаты сохранены в {output_file}")
