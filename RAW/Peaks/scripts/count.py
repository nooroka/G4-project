import sys
op = open(sys.argv[1],"r")
w =  open(sys.argv[2],"w")
#op = open("/data/nooroka/grant/punkt1/GSM3003539/GSM3003539_quadr_7_4.bed","r")
#w = open("quadr7_chain180424.bed","w")
for line in op:
    line = line.strip()
    line = line.split()
    line11 = line[0].split(":")
    line111 = line11[1].split("-")
    print(line111[0], line[1])
    a = int(line111[0])+int(line[1])-10#если бы был txt-формат, надо было еще 1 прибавить
    b = int(line111[0])+int(line[2])+10
    w.write(str(line11[0])+"\t"+str(a)+"\t"+str(b)+"\t"+str(line[5])+"\n")
w.close()
op.close()

