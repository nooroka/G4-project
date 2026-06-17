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

op = open(sys.argv[1], "r")
w3 = open(
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_new_{}2defnongenes_less_50_control_39.bed".format(sys.argv[2]),
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

cmd = (
    "bedtools intersect "
    "-a <(awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}' "
    "<(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz)) "
    "-b /data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_new_{0}2defnongenes_less_50_control_39.bed "
    "-wa -wb | awk '!seen[$4]++' "
    "> /data/nooroka/grant/punkt3/stage2/intmut/intmuthg19{0}_genome_control.bed"
).format(sys.argv[2])

subprocess.run(cmd, shell=True, executable="/bin/bash")

d1 = count_lines_fast(
    '/data/nooroka/grant/punkt3/stage2/intmut/intmuthg19{}_genome_control.bed'.format(sys.argv[2])
)
d11 = d1

# Исправлено: сначала проверяем total и d1, потом вычисляем d55
if total == 0 or d1 == 0:
    w.write("chr{}\tnon G4 motif\taverage density\t0\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], a
    ))
else:
    d55 = d1 / total          # плотность (дробное число, int() не применяем)   # исправлено: int(d55) заменён на d55
    w.write("chr{}\tnon G4 motif\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], d55, a
    ))

w.close()
