#!/bin/bash

# Директория с файлами
DIR="/data/nooroka/grant/punkt3/stage2/scripts/temp"
DIR2="/data/nooroka/grant/punkt3/bed-37"
# Перебираем все хромосомы
for chr in {1..22} X Y; do
    # Определяем имена входных файлов
    dbsnp_file="${DIR2}/bed_chr_${chr}_sorted.bed"
    quadr_file="${DIR}/quadr_chr${chr}.bed"
    
    # Проверяем существование файлов
    if [[ -f "$dbsnp_file" && -f "$quadr_file" ]]; then
        # Имя выходного файла
        output_file="${DIR}/intersected_chr${chr}_bed.bed"
        
        # Пересекаем файлы с помощью bedtools intersect
        bedtools intersect -a "$dbsnp_file" -b "$quadr_file" > "$output_file"
        
        echo "Обработана хромосома $chr, результат в $output_file"
    else
        echo "Файлы для хромосомы $chr не найдены, пропускаем"
    fi
done

echo "Обработка завершена"
