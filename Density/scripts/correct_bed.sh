#!/bin/bash

# Скрипт для исправления BED файлов
# Удаляет пустые строки и заменяет пробелы на табуляции

echo "Начало обработки BED файлов..."

# Исправить все файлы с маской GSM_hg196_un_*_39_my_minus.bed
for file in ../../../punkt1/GSM/GSM_hg196_un_*_39_my_minus.bed; do
    if [ -f "$file" ]; then
        echo "Обработка файла: $file"
        awk 'NF >= 3 && $2 ~ /^[0-9]+$/ && $3 ~ /^[0-9]+$/ {
            for(i=1; i<=NF; i++) {
                printf "%s%s", $i, (i<NF ? "\t" : "\n")
            }
        }' "$file" > "${file}.fixed"
        
        if [ -s "${file}.fixed" ]; then
            mv "${file}.fixed" "$file"
            echo "  ✓ Файл $file успешно исправлен"
        else
            echo "  ✗ Ошибка: исправленный файл пустой, оригинал сохранён"
            rm "${file}.fixed"
        fi
    fi
done

echo "Готово! Все файлы обработаны."
