#!/bin/bash

# Директория с файлами
INPUT_DIR="temp"
OUTPUT_DIR="temp"

# Хромосомы для обработки (1-22, X, Y)
CHROMOSOMES=({1..22} X Y)

# Обрабатываем каждую хромосому
for chrom in "${CHROMOSOMES[@]}"; do
    input_file="${INPUT_DIR}/intersected_chr${chrom}_bed.bed"
    sorted_file="${INPUT_DIR}/intersected_chr${chrom}_bed.sorted.bed"  # Временный отсортированный файл
    output_file="${OUTPUT_DIR}/merged_intersected_chr${chrom}_bed.bed"
    
    # Проверяем существование входного файла
    if [[ ! -f "$input_file" ]]; then
        echo "Файл $input_file не найден, пропускаем..."
        continue
    fi
    
    # Сортируем BED-файл с помощью bedtools sort
    echo "Сортируем файл для хромосомы $chrom..."
    bedtools sort -i "$input_file" > "$sorted_file"
    
    # Проверяем успешность сортировки
    if [[ $? -ne 0 ]]; then
        echo "Ошибка при сортировке $input_file"
        continue
    fi
    
    # Выполняем bedtools merge на отсортированном файле
    echo "Обрабатываем хромосому $chrom..."
    bedtools merge -i "$sorted_file" > "$output_file"
    
    # Проверяем успешность выполнения
    if [[ $? -eq 0 ]]; then
        echo "Успешно создан $output_file"
        # Удаляем временный отсортированный файл (опционально)
       # rm "$sorted_file"
    else
        echo "Ошибка при обработке $sorted_file"
    fi
done

echo "Все операции завершены"
