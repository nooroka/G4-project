op = open("GSM3003540_with_quadruplexes.fasta","r")
w = open("GSM3003540_with_quadruplexes.bed", "w")
for line in op:
    line = line.strip()
    if ">" in line:
        line = line.split(":")
        line2 = line[1].split("-")
        w.write(str(line[0][1:])+"\t"+str(line2[0])+"\t"+str(line2[1])+"\n")
w.close()
op.close()

