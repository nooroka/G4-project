import os
import gzip
import subprocess
from collections import defaultdict
import sys

w = open(sys.argv[4], "a")

def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    if filepath.endswith(".gz"):
        cmd = "zcat {} | wc -l".format(filepath)
        result = subprocess.run(
            cmd, shell=True, executable="/bin/bash",
            capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count

def run_count(bed_a, bed_b_path):
    """
    bedtools intersect(-a bed_a фикс координат, -b bed_b_path)
    | sort -k4,4 -u | wc -l
    Возвращает число уникальных пересечений (по 4-й колонке).
    Если bed_a в .gz — читаем через zcat перед awk (process substitution).
    """
    a_src = "zcat {}".format(bed_a) if bed_a.endswith(".gz") else "cat {}".format(bed_a)
    cmd = (
        "bedtools intersect "
        "-a <({a_src} | awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}') "
        "-b {b} "
        "| sort -k4,4 -T /tmp -S 2G -u "
        "| wc -l"
    ).format(a_src=a_src, b=bed_b_path)
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        capture_output=True, text=True, check=True
    )
    return int(result.stdout.strip())

bed_chr = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[3])

# ── 1. Первый bedtools: мутации (argv1) × гены ───────────────────────────────
count_intersections_mut = run_count(bed_chr, sys.argv[1])

# ── 2. Читаем sys.argv[2], пишем gccoords (обычный .bed) ───────────────────
op2 = open(sys.argv[1], "r")
sum_gc = 0
op = open(sys.argv[2], "r")

gccoords_path = (
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{}2defhg19_{}_all_loop7_control1_50_more_equal.bed".format(sys.argv[3], sys.argv[5])
)

w3 = open(gccoords_path, "wt")
a = ""
sum1 = 0
for line in op:
    line = line.strip().split()
    a = line[6]
    line77 = int(line[7][1:-1])
    line88 = line[8][:-1]
    b = int(line88) - line77
    sum1 += b
    w3.write("chr{}\t{}\t{}\n".format(sys.argv[3], line77, line88))
w3.close()
op.close()

count_lines_gc = count_lines_fast(sys.argv[2])

# ── 3. Второй bedtools: мутации × GC-координаты ─────────────────────────────
count_intersections_gc = run_count(bed_chr, gccoords_path)

for line2 in op2:
    line2 = line2.strip().split()
    sum22 = int(line2[2]) - int(line2[1])
    sum_gc += sum22
op2.close()

count_lines_mut = count_lines_fast(sys.argv[1])

if a == "":
    a = 0
if count_lines_gc == 0:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t0"
        "\taverage G4 motif/interval length\t{}\n".format(sys.argv[3], a)
    )
else:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t{}"
        "\taverage G4 motif/interval length\t{}\n".format(
            sys.argv[3], float(int(count_intersections_gc) / int(sum1)), a
        )
    )
w.write(
    "chr{}\tG4 motif all\taverage density\t{}"
    "\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[3],
        float(int(count_intersections_mut) / int(sum_gc)),
        float(int(sum_gc) / int(count_lines_mut)),
    )
)
w.close()
