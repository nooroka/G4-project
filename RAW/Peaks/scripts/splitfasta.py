import sys
from Bio import SeqIO
for i in range(1,25,1):
    dict1 = {}
    handle = open("/data/nooroka/grant/punkt1/stage2/fasta/{}".format(sys.argv[1]),"r")
    for record in SeqIO.parse(handle, "fasta"):
        id1 = record.id.split(":")
        if int(id1[0][3:]) == int(i):
            sysa = sys.argv[1].split(".")
            w = open("/data/nooroka/grant/punkt1/stage2/fasta/{}_{}.fasta".format(sysa[0],i),"a")
            w.write(">"+str(record.id)+"\n"+str(record.seq)+"\n")
            w.close()
    handle.close()
