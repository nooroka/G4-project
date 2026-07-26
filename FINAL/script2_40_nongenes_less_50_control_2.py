import os
import subprocess
from collections import defaultdict
import sys

w = open(sys.argv[3], "a")


def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count


def run_count(bed_a_gz, bed_b_path):
    """
    bedtools intersect(-a zcat(bed_a_gz) фикс координат, -b bed_b_path)
    | sort -k4,4 -u | wc -l
    Возвращает число уникальных пересечений (по 4-й колонке).
    """
    cmd = (
        "bedtools intersect "
        "-a <(zcat {a} "
        "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1') "
        "-b {b} "
        "| sort -k4,4 -T /tmp -S 2G -u "
        "| wc -l"
    ).format(a=bed_a_gz, b=bed_b_path)
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        capture_output=True, text=True, check=True
    )
    return int(result.stdout.strip())


op = open(sys.argv[1], "r")
w3 = open(
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_new_{}2defnongenes_less_50_control_40.bed".format(sys.argv[2]),
    "w"
)
a = ""
total = 0
for line in op:
    line = line.strip().split()
    a = line[6]
    line77 = int(line[7][1:-1])
    line88 = line[8][:-1]
    k = int(line88) - int(line77)
    total += k
    w3.write("chr{}\t{}\t{}\n".format(sys.argv[2], line77, line88))
w3.close()
op.close()

if a == "":
    a = 0

d5 = count_lines_fast(sys.argv[1])  # исправлено: убран лишний format()

bed_chr_gz = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[2])
gccoords_path = "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_new_{}2defnongenes_less_50_control_40.bed".format(sys.argv[2])

d1 = run_count(bed_chr_gz, gccoords_path)
d11 = d1

# Исправлено: сначала проверяем total и d1, потом вычисляем d55
if total == 0 or d1 == 0:
    w.write("chr{}\tnon G4 motif\taverage density\t0\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], a
    ))
else:
    d55 = d1 / total          # плотность (дробное число, int() не применяем)
    w.write("chr{}\tnon G4 motif\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], d55, a
    ))
w.close()
