op = open("../hg19_new_quadr_loop7.bed","r")
w = open("../hg19_new_quadr_loop7_bed.bed","w")
for line in op:
    line = line.strip()
    line = line.split()
    if len(line)==7:
        w.write(str(line[0])+"\t"+str(line[1])+"\t"+str(line[2])+"\n")
w.close()
op.close()
