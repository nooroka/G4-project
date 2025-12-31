from Bio import SeqIO
op = open("/data/nooroka/grant/punkt1/GSM3003540/GSM3003540_quadr_7_7.bed","r")
list1 = []
for line in op:
    line = line.strip()
    line = line.split()
    list1.append(str(line[0]))
op.close()
#print(list1)
dict1 = {}
handle = open("/data/nooroka/grant/punkt1/GSM3003540/GSM3003540_Homo_all_w15_th-1.hits.max.K.w50.35.fasta")
for record in SeqIO.parse(handle, "fasta") :
    if record.id in list1:
        dict1[record.id] = str(record.seq)
handle.close()
w = open("GSM3003540_with_quadruplexes.fasta","w")
for key in dict1:
    w.write(">"+str(key)+"\n"+str(dict1[key])+"\n")
w.close()

