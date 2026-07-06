#!/bin/bash

# 1.1: исправляем регионы
tmp1=$(mktemp)
tmp2=$(mktemp)

awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' "$1" > "$tmp1"

# 1.2: пересечения с подсчётом
bedtools intersect -c -a "$tmp1" -b "$2" > "$tmp2"

# 1.3: длина и плотность
awk 'BEGIN{OFS="\t"} {
    len=$3-$2
    density_per_kb = ($NF==0?0:$NF/(len/1000))
    print $0, len, density_per_kb
}' "$tmp2" > "$3"

rm -f "$tmp1" "$tmp2"
