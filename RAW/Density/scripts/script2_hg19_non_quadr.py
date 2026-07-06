import os
import subprocess
from collections import defaultdict
import sys #поменяли wc -l одно из
w = open(sys.argv[3],"a")

def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count
op = open(sys.argv[1],"r")
w3 = open("/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defhg19_genome_control.bed".format(sys.argv[2]),"w")
a  = ""
for line in op:
        line = line.strip()
        line = line.split()
        a = line[6]
        #print("line "+str(line))
        line77 = int(line[7][1:-1])
        line88 = line[8][:-1]
        #print("line77-88 "+str(line77)+"\t"+str(line88))
        w3.write("chr{}".format(sys.argv[2])+"\t"+str(line77)+"\t"+str(line88)+"\n")
w3.close()
op.close()
d5 = count_lines_fast(format(sys.argv[1]))
os.system("sort -k 4,4 -s  /data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defhg19_genome_control.bed > /data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}_undefhg19_genome_control.bed".format(sys.argv[2],sys.argv[2]))
cmd = """bedtools intersect -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' /data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed) -b /data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}_undefhg19_genome_control.bed -wa -wb | awk '!seen[$4]++' > /data/nooroka/grant/punkt3/stage2/intmut/intmuthg19{}_genome_control.bed""".format(
    sys.argv[2], sys.argv[2], sys.argv[2]
)
subprocess.run(cmd, shell=True, executable="/bin/bash")
d1 =count_lines_fast('/data/nooroka/grant/punkt3/stage2/intmut/intmuthg19{}_genome_control.bed'.format(sys.argv[2]))
d11 = d1
if a=="":
    a = 0
d55 = int(d5)*int(a)
if d55==0: 
    w.write("chr{}".format(sys.argv[2])+"\t"+"non G4 motif"+"\t"+"average density"+"\t"+"0"+"\taverage G4 motif/interval length"+"\t"+str(a)+"\n")
else:
    w.write("chr{}".format(sys.argv[2])+"\t"+"non G4 motif"+"\t"+"average density"+"\t"+str(float(int(d11)/int(d55)))+"\taverage G4 motif/interval length"+"\t"+str(a)+"\n")
w.close()

