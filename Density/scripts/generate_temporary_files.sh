#!/bin/bash

QUAD_BED="/data/nooroka/grant/punkt1/stage2/sorted/quadr7_chain180424_merged2_sorted_39_copy.bed"
DBSNP_DIR="/mnt/work/nooroka/dbSNP_chromosomes"
TEMP_DIR="temp_files"
OUTPUT="dbsnp_density_per_chrom_39.txt"

# Создаем директории и выходной файл
mkdir -p "$TEMP_DIR"
echo -e "Chromosome\tQuadLength(bp)\tSNP_count\tDensity(SNP/kb)" > "$OUTPUT"

process_chromosome() {
    local CHR=$1
    
    # 1. Извлекаем квадруплексы
    awk -v chr="chr$CHR" '$1 == chr' "$QUAD_BED" > "${TEMP_DIR}/quad_chr${CHR}.bed"
    [ ! -s "${TEMP_DIR}/quad_chr${CHR}.bed" ] && return 1

    # 2. Конвертируем VCF в BED
    zcat "${DBSNP_DIR}/chr${CHR}.vcf.gz" | awk -v chr="chr$CHR" '!/^#/ {print chr"\t"$2-1"\t"$2}' > "${TEMP_DIR}/dbsnp_chr${CHR}.bed"

    # 3. Сортируем файлы
    sort -k1,1 -k2,2n "${TEMP_DIR}/quad_chr${CHR}.bed" > "${TEMP_DIR}/quad_sorted_chr${CHR}.bed"
    sort -k1,1 -k2,2n "${TEMP_DIR}/dbsnp_chr${CHR}.bed" > "${TEMP_DIR}/dbsnp_sorted_chr${CHR}.bed"

    # 4. Облегченный метод поиска пересечений с join
    join -1 1 -2 1 \
         -o '1.1,1.2,1.3,2.2' \
         "${TEMP_DIR}/quad_sorted_chr${CHR}.bed" \
         "${TEMP_DIR}/dbsnp_sorted_chr${CHR}.bed" \
        | awk '$4 >= ($2 + 1) && $4 <= $3' \
        | cut -f1-3 | uniq -c \
        | awk '{print $2"\t"$3"\t"$4"\t"$1}' > "${TEMP_DIR}/overlap_chr${CHR}.bed"

    # 5. Расчет статистик
    TOTAL_LEN=$(awk '{sum += $3 - $2} END {print sum}' "${TEMP_DIR}/quad_sorted_chr${CHR}.bed")
    TOTAL_SNP=$(awk '{sum += $4} END {print sum}' "${TEMP_DIR}/overlap_chr${CHR}.bed")
    
    DENSITY=$(awk -v snp="$TOTAL_SNP" -v len="$TOTAL_LEN" 'BEGIN {print (len > 0) ? snp / (len / 1000) : 0}')
    echo -e "chr${CHR}\t${TOTAL_LEN}\t${TOTAL_SNP}\t${DENSITY}" >> "$OUTPUT"

    # 6. Очистка временных файлов
    rm "${TEMP_DIR}/quad_chr${CHR}.bed" "${TEMP_DIR}/dbsnp_chr${CHR}.bed" \
       "${TEMP_DIR}/quad_sorted_chr${CHR}.bed" "${TEMP_DIR}/dbsnp_sorted_chr${CHR}.bed" \
       "${TEMP_DIR}/overlap_chr${CHR}.bed"
}

# Обрабатываем хромосомы параллельно
export QUAD_BED DBSNP_DIR TEMP_DIR OUTPUT
export -f process_chromosome

parallel --halt soon,fail=1 --jobs 4 process_chromosome ::: {1..22} X Y

# Альтернатива без parallel (последовательная обработка):
# for CHR in {1..22} X Y; do
#     process_chromosome "$CHR"
# done

