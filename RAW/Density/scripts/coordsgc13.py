import sys
#w = open("KEK.txt","w")
#for i in range(1,25,1):
op = open(sys.argv[1],"r")
w = open(sys.argv[2],"w")
    #w = open("gccoords_promoter_{}".format("_"+str(sysa[3])+"_"+str(sysa[5])),"w")
for line in op:
        line = line.strip()
        line2 = line.split()
        if float(line2[1]) >= 0.5:
            w.write(str(line)+"\n")
w.close()
op.close()

