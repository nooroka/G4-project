#!/bin/bash

QUAD_BED="/data/nooroka/grant/punkt1/stage2/sorted/quadr7_chain180424_merged2_sorted_39_copy.bed"
DBSNP_DIR="/mnt/work/nooroka/dbSNP_chromosomes"
OUTPUT="dbsnp_density_per_chrom_39.txt"

echo -e "Chromosome\tQuadLength(bp)\tSNP_count\tDensity(SNP/kb)" > "$OUTPUT"

for CHR in {1..22} X Y; do
    DBSNP_FILE="${DBSNP_DIR}/chr${CHR}.vcf.gz"
    
    if [ ! -f "$DBSNP_FILE" ]; then
        echo "Файл dbSNP для chr${CHR} не найден, пропускаем."
        continue
    fi

    # 1. Извлекаем квадруплексы текущей хромосомы
    awk -v chr="chr${CHR}" '$1 == chr' "$QUAD_BED" > "quad_chr${CHR}.bed"

    if [ ! -s "quad_chr${CHR}.bed" ]; then
        echo "Нет квадруплексов на chr${CHR}, пропускаем."
        rm "quad_chr${CHR}.bed"
        continue
    fi

    # 2. Конвертируем VCF в BED (chr, start=pos-1, end=pos)
    zcat "$DBSNP_FILE" | awk -v chr="chr${CHR}" '!/^#/ {print chr"\t"$2-1"\t"$2}' > "dbsnp_chr${CHR}.bed"

    # 3. Сортируем оба файла по координатам
    sort -k1,1 -k2,2n "quad_chr${CHR}.bed" > "quad_sorted.bed"
    sort -k1,1 -k2,2n "dbsnp_chr${CHR}.bed" > "dbsnp_sorted.bed"

    # 4. Альтернативный метод пересечения (без bedtools)
    awk '
        BEGIN {
            # Загружаем SNP в массив ranges[chr][pos]
            while ((getline < "dbsnp_sorted.bed") > 0) {
                chr = $1
                pos = $3  # BED-формат: $2=pos-1, $3=pos
                if (!(chr in ranges)) {
                    ranges[chr][pos] = 1
                } else {
                    ranges[chr][pos] = 1
                }
            }
        }
        {
            # Для каждого квадруплекса считаем SNP в его пределах
            chr = $1
            start = $2 + 1  # BED: 0-based -> 1-based
            end = $3
            count = 0
            
            if (chr in ranges) {
                # Проходим по всем SNP в этом диапазоне
                for (pos in ranges[chr]) {
                    if (pos >= start && pos <= end) {
                        count++
                    }
                }
            }
            print $0 "\t" count
        }
    ' "quad_sorted.bed" > "overlap_chr${CHR}.bed"

    # 5. Расчет статистик
    TOTAL_LEN=$(awk '{sum += $3 - $2} END {print sum}' "quad_sorted.bed")
    TOTAL_SNP=$(awk '{sum += $4} END {print sum}' "overlap_chr${CHR}.bed")

    if [ "$TOTAL_LEN" -eq 0 ]; then
        DENSITY=0
    else
        DENSITY=$(echo "scale=17; $TOTAL_SNP / ($TOTAL_LEN / 1000)" | bc)
    fi

    echo -e "chr${CHR}\t${TOTAL_LEN}\t${TOTAL_SNP}\t${DENSITY}" >> "$OUTPUT"

    # 6. Удаление временных файлов
    rm "quad_chr${CHR}.bed" "dbsnp_chr${CHR}.bed" \
       "quad_sorted.bed" "dbsnp_sorted.bed" "overlap_chr${CHR}.bed"
done
