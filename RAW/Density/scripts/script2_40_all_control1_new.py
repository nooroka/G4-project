import os
import subprocess
from collections import defaultdict
import sys

w = open(sys.argv[4], "a")

def count_lines_fast(filepath):
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count

# resultgene — читаем stdout, без записи на диск
cmd_resultgene = """bedtools intersect -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' /data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed) -b {} -wa -wb""".format(sys.argv[3], sys.argv[1])
result_resultgene = subprocess.run(cmd_resultgene, shell=True, executable="/bin/bash", capture_output=True, text=True)

# uniq + awk '!seen[$4]++' — применяем к stdout через pipe
cmd_un = "sort -k 4,4, -s | awk '!seen[$4]++'"
result_un = subprocess.run(cmd_un, shell=True, executable="/bin/bash", input=result_resultgene.stdout, capture_output=True, text=True)
d22 = result_un.stdout.count("\n")  # аналог count_lines_fast для resultgene_un

op2 = open(sys.argv[1], "r")
d44 = 0
op = open(sys.argv[2], "r")
w3 = open("/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defhg19_40_all_loop7_control1_new.bed".format(sys.argv[3]), "w")
a = ""

for line in op:
    line = line.strip().split()
    a = line[6]
    line77 = int(line[7][1:-1])
    line88 = line[8][:-1]
    w3.write("chr{}\t{}\t{}\n".format(sys.argv[3], line77, line88))

w3.close()
op.close()

d5 = count_lines_fast(sys.argv[2])
# intmut — читаем stdout, без записи на диск
cmd_intmut = """bedtools intersect -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' /data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed) -b /data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}_2defhg19_40_all_loop7_control1_new.bed -wa -wb | awk '!seen[$4]++'""".format(
    sys.argv[3], sys.argv[3]
)
result_intmut = subprocess.run(cmd_intmut, shell=True, executable="/bin/bash", capture_output=True, text=True)
d11 = result_intmut.stdout.count("\n")  # аналог count_lines_fast для intmut

for line2 in op2:
    line2 = line2.strip().split()
    sum22 = int(line2[2]) - int(line2[1])
    d44 += sum22
op2.close()

d6 = count_lines_fast(sys.argv[1])
if a == "":
    a = 0

d55 = int(d5) * int(a)
print("d11-55-22-4 " + str(d11) + "\t" + str(d55) + "\t" + str(d22) + "\t" + str(d4))
if d55 == 0:
    w.write("chr{}\tnon G4 motif\taverage density\t0\taverage G4 motif/interval length\t{}\n".format(sys.argv[3], a))
else:
    w.write("chr{}\tnon G4 motif\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[3], float(int(d11) / int(d55)), a))

w.write("chr{}\tG4 motif all\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
    sys.argv[3], float(int(d22) / int(d4)), float(int(d4) / int(d66))))

w.close()
