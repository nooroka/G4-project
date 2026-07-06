import os
import subprocess
from collections import defaultdict
import sys #поменяли wc -l одно из
w = open(sys.argv[3],"a")
cmd = """bedtools intersect -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' <(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz)) -b {} -wa -wb > /data/nooroka/grant/punkt3/stage2/resultgene/resultgenehg19{}_genes_no_rnapIII_control_39.bed""".format(sys.argv[2], sys.argv[1], sys.argv[2])

subprocess.run(cmd, shell=True, executable="/bin/bash")
def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count
os.system("sort -k4,4 -s /data/nooroka/grant/punkt3/stage2/resultgene/resultgenehg19{}_genes_no_rnapIII_control_39.bed | awk  '!seen[$4]++' > /data/nooroka/grant/punkt3/stage2/resultgene/resultgenehg19{}_genes_no_rnapIII_control_39_un.bed".format(sys.argv[2],sys.argv[2])) #мб не надо, проверить схожесть файлов
d4 = 0
d2 =count_lines_fast('/data/nooroka/grant/punkt3/stage2/resultgene/resultgenehg19{}_genes_no_rnapIII_control_39_un.bed'.format(sys.argv[2]))
op2 = open(sys.argv[1],"r")
for line2 in op2:
       # d2 +=1
        line2 = line2.strip()
        line2 = line2.split()
        sum22 = int(line2[2])-int(line2[1])
        d4+=sum22
op2.close()
subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
d6 =count_lines_fast('{}'.format(sys.argv[1]))
d22 = d2
d66 = d6
w.write("chr{}".format(sys.argv[2])+"\t"+"G4 motif all"+"\t"+"average density"+"\t"+str(float(int(d22)/int(d4)))+"\taverage G4 motif/interval length"+"\t"+str(float(int(d4)/int(d66)))+"\n")
w.close()

