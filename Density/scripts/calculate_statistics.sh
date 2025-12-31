#!/bin/bash

TEMP_DIR="temp_files" 
OUTPUT="dbsnp_density_per_chrom_39.txt"

echo -e "Chromosome\tQuadLength(bp)\tSNP_count\tDensity(SNP/kb)" > "$OUTPUT"

for CHR in {1..22} X Y; do
    if [ ! -f "${TEMP_DIR}/overlap_chr${CHR}.bed" ] || [ ! -f "${TEMP_DIR}/quad_sorted_chr${CHR}.bed" ]; then
        continue
    fi

    # 1. Расчет статистик
    TOTAL_LEN=$(awk '{sum += $3 - $2} END {print sum}' "${TEMP_DIR}/quad_sorted_chr${CHR}.bed")
    TOTAL_SNP=$(awk '{sum += $4} END {print sum}' "${TEMP_DIR}/overlap_chr${CHR}.bed")

    if [ "$TOTAL_LEN" -eq 0 ]; then
        DENSITY=0
    else
        DENSITY=$(echo "scale=17; $TOTAL_SNP / ($TOTAL_LEN / 1000)" | bc)
    fi

    echo -e "chr${CHR}\t${TOTAL_LEN}\t${TOTAL_SNP}\t${DENSITY}" >> "$OUTPUT"
done

