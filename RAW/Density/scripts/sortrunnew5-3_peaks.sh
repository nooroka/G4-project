#!/bin/bash
# 1.1: подготовим исправленный файл regions_peaks (как у вас раньше)
awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' $1 > regions_peaks.fixed.bed

# 1.2: для подсчёта числа мутаций, пересекающихся с каждым регионом:
bedtools intersect -c -a regions_peaks.fixed.bed -b $2 > regions_peaks.with_counts.bed
# Формат: <region fields> <count>

# 1.3: добавить колонку с длиной региона и плотностью (мутаций на килобазу)
awk 'BEGIN{OFS="\t"} {len=$3-$2; density_per_kb = ($NF==0?0:$NF/(len/1000)); print $0, len, density_per_kb}' regions_peaks.with_counts.bed > $3
rm regions_peaks.fixed.bed
rm regions_peaks.with_counts.bed
