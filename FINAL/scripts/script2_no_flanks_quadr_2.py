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


bed_chr_gz = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[2])

d2 = run_count(bed_chr_gz, sys.argv[1])

d4 = 0
op2 = open(sys.argv[1], "r")
for line2 in op2:
    line2 = line2.strip().split()
    sum22 = int(line2[2]) - int(line2[1])
    d4 += sum22
op2.close()

d6 = count_lines_fast(sys.argv[1])

d22 = d2
d66 = d6

w.write(
    "chr{}".format(sys.argv[2]) + "\t" + "G4 motif all" + "\t" + "average density" + "\t"
    + str(float(int(d22) / int(d4))) + "\taverage G4 motif/interval length" + "\t"
    + str(float(int(d4) / int(d66))) + "\n"
)
w.close()
