#!/bin/bash

[ $# -ne 3 ] && echo "Usage: script.sh regions.bed mutations.bed output.bed" && exit 1

# 1.1: исправляем регионы где end <= start
awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' $1 \
  | sort -k1,1 -k2,2n > regions.fixed.bed

# 1.2: сортируем мутации и считаем пересечения
sort -k1,1 -k2,2n $2 > mutations.sorted.bed
bedtools intersect -c -sorted -a regions.fixed.bed -b mutations.sorted.bed > regions.with_counts.bed

# 1.3: добавляем длину региона, плотность и самую частую длину для хромосомы
awk 'BEGIN{OFS="\t"}
# Первый проход: считаем частоты длин по хромосомам
NR==FNR {
    len = $3 - $2
    freq[$1 SUBSEP len]++
    if (freq[$1 SUBSEP len] > max[$1]) {
        max[$1] = freq[$1 SUBSEP len]
        mode[$1] = len
    }
    next
}
# Второй проход: печатаем с новыми колонками
{
    len = $3 - $2
    density_per_kb = (len==0 ? 0 : $NF/(len/1000))
    print $0, mode[$1], density_per_kb
}' regions.with_counts.bed regions.with_counts.bed > $3

rm regions.fixed.bed mutations.sorted.bed regions.with_counts.bed
