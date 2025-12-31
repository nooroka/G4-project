import os
import sys
op = open(sys.argv[1],"r")
w = open(sys.argv[2],"w")
for line in op:
    line = line.strip()
    line2 = line.split()
    line22 = line2[0].split(":")#смотрим интервалы, откуда пришли
    line33 = line22[1].split("-")
    w.write(str(line22[0])+"\t"+str(line33[0])+"\t"+str(line33[1][:-2])+"\n")
w.close()
op.close()
#os.system("uniq GSM_hg196.bed > GSM_hg196_un.bed")

