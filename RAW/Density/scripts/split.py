
op = open("hg19_new.fna.bed","r")
for line in op:
    line = line.strip()
    line = line.split()
    w = open("hg19/hg19_new{}.fna.bed".format(line[0][3:]),"w")
    w.write(str(line[0])+"\t"+str(line[1])+"\t"+str(line[2]))
    w.close()
op.close()
