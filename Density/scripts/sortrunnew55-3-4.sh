#!/bin/bash
set -euo pipefail


tmp_fixed="${3}.fixed.$$.bed"
tmp_counts="${3}.with_counts.$$.bed"
awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' "$1" > "$tmp_fixed"

bedtools intersect -c -a "$tmp_fixed" -b "$2" | awk '$NF > 0' > "$tmp_counts"
awk 'BEGIN{OFS="\t"} {
    count = $NF
    NF--
    len = $3 - $2
    density_per_kb = (len > 0 ? count / (len / 1000) : 0)
    print $0, count, len, density_per_kb
}' "$tmp_counts" > "$3"
