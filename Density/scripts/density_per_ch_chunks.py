#!/usr/bin/env python3
import sys
import math
import hashlib
import csv
from collections import defaultdict

if len(sys.argv) < 2:
    print("Usage: python per_chrom_density.py input.bed [out.csv]")
    sys.exit(1)

inp = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "per_chrom_density.csv"

# ── определяем индексы нужных колонок по первой строке ────────────────────
with open(inp, 'r') as fh:
    for line in fh:
        parts = line.split()
        if len(parts) >= 3:
            ncols = len(parts)
            break
    else:
        print("Ошибка: файл пуст или не читается", file=sys.stderr)
        sys.exit(1)

idx_chrom  = 0
idx_count  = ncols - 3
idx_length = ncols - 2

# ── однопроходное чтение: только бегущие суммы ────────────────────────────
count_sums   = defaultdict(int)
length_lists = defaultdict(list)

with open(inp, 'r') as fh:
    for lineno, line in enumerate(fh, 1):
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            chrom  = parts[idx_chrom]
            count  = int(parts[idx_count])
            length = float(parts[idx_length])
        except ValueError:
            if lineno == 1:
                continue  # заголовок
            print(f"[WARN] line {lineno}: пропускаем: {line.rstrip()}", file=sys.stderr)
            continue
        if count < 0 or length < 0:
            print(f"[WARN] line {lineno}: отрицательное значение — пропускаем", file=sys.stderr)
            continue
        count_sums[chrom]    += count
        length_lists[chrom].append(length)

if not count_sums:
    print("Ошибка: не прочитано ни одной строки", file=sys.stderr)
    sys.exit(1)

length_sums = {ch: math.fsum(v) for ch, v in length_lists.items()}
del length_lists  # освобождаем память сразу

# ── сортировка ────────────────────────────────────────────────────────────
def chrom_key(ch):
    s = ch.lstrip('chr')
    if s.isdigit(): return int(s)
    if s == 'X':    return 1000
    if s == 'Y':    return 1001
    return 2000 + int(hashlib.md5(s.encode()).hexdigest(), 16) % 1000

chroms = sorted(count_sums, key=chrom_key)

# ── запись ────────────────────────────────────────────────────────────────
total_count  = 0
total_length = []

with open(out, 'w', newline='') as fh:
    w = csv.writer(fh, delimiter='\t')
    w.writerow(['chrom', 'total_count', 'total_length_bp', 'density_per_kb'])
    for ch in chroms:
        tc      = count_sums[ch]
        tl      = length_sums[ch]
        density = tc / tl if tl > 0 else 0.0
        w.writerow([ch, tc, f'{tl:.17f}', f'{density:.18f}'])
        print(f"{ch}\t{tc}\t{tl:.2f}\t{density:.6f}")
        total_count  += tc
        total_length.append(tl)

print("Wrote:", out)

total_length_genome = math.fsum(total_length)
genome_density = total_count / total_length_genome \
                 if total_length_genome > 0 else 0.0

with open(out + ".genome_summary.txt", 'w') as fh:
    fh.write("total_count\ttotal_length_bp\tdensity_per_kb\n")
    fh.write(f"{total_count}\t{total_length_genome:.17f}\t{genome_density:.18f}\n")

print("Wrote:", out + ".genome_summary.txt")
