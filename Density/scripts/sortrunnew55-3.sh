#!/bin/bash
awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' $1 > regions.fixed.bed

bedtools intersect -c -a regions.fixed.bed -b $2 > regions.with_counts.bed
awk 'BEGIN{OFS="\t"} {len=$3-$2; density_per_kb = ($NF==0?0:$NF/(len/1000)); print $0, len, density_per_kb}' regions.with_counts.bed > $3
rm regions.fixed.bed
rm regions.with_counts.bed
