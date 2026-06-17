#!/bin/bash
set -euo pipefail

tmp_fixed="${3}.fixed.bed"
tmp_counts="${3}.with_counts.bed"

# 1.1
awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' "$1" > "$tmp_fixed"

# 1.2
bedtools intersect -c -a "$tmp_fixed" -b "$2" | awk '$NF > 0' > "$tmp_counts"

# 1.3
awk 'BEGIN{OFS="\t"} {len=$3-$2; density_per_kb = ($NF==0?0:$NF/(len/1000)); print $0, len, density_per_kb}' \
    "$tmp_counts" > "$3"

rm -f "$tmp_fixed" "$tmp_counts"
