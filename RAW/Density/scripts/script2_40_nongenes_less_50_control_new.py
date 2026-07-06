import os
import subprocess
import sys

w = open(sys.argv[3], "a")

def count_lines_fast(filepath):
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count

op = open(sys.argv[1], "r")
w3 = open("/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defnongenes_control_less_50_40.bed".format(sys.argv[2]), "w")
a = ""

for line in op:
    line = line.strip().split()
    a = line[6]
    line77 = int(line[7][1:-1])
    line88 = line[8][:-1]
    w3.write("chr{}\t{}\t{}\n".format(sys.argv[2], line77, line88))

w3.close()
op.close()

d5 = count_lines_fast(sys.argv[1])
# bedtools без записи intmut на диск — результат читаем из stdout
cmd = """bedtools intersect -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' /data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed) -b /data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}_2defnongenes_control_less_50_40.bed -wa -wb | awk '!seen[$4]++'""".format(
    sys.argv[2], sys.argv[2]
)

result = subprocess.run(cmd, shell=True, executable="/bin/bash", capture_output=True, text=True)

d1 = result.stdout.count("\n")  # считаем строки из памяти, без файла intmut
d11 = d1

if a == "":
    a = 0

d55 = int(d5) * int(a)

if d55 == 0:
    w.write("chr{}\tnon G4 motif\taverage density\t0\taverage G4 motif/interval length\t{}\n".format(sys.argv[2], a))
else:
    w.write("chr{}\tnon G4 motif\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], float(int(d11) / int(d55)), a))

w.close()
