#!/bin/bash
set -euo pipefail

# создаём уникальную временную директорию для этого конкретного запуска
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

regions_fixed="$workdir/regions.fixed.bed"
regions_counts="$workdir/regions.with_counts.bed"

# 1.1: исправляем регионы, где end <= start
awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' "$1" > "$regions_fixed"

# 1.2: считаем число мутаций, пересекающихся с каждым регионом
bedtools intersect -c -a "$regions_fixed" -b "$2" > "$regions_counts"
# Формат: <region fields> <count>

# 1.3: добавляем длину региона и плотность (мутаций на килобазу)
awk 'BEGIN{OFS="\t"} {
    len = $3 - $2
    density_per_kb = ($NF == 0 ? 0 : $NF / (len/1000))
    print $0, len, density_per_kb
}' "$regions_counts" > "$3"

# временные файлы удалятся автоматически через trap при выходе
