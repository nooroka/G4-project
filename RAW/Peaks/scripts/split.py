import sys
op = open(sys.argv[1],"r")
#syssplit = sys.argv[1].split(".")
for line in op:
    line = line.strip()
    line2 = line.split()
    a = line2[0][3:]
    if a == str(sys.argv[3]):
        w = open(sys.argv[2],"a")
        w.write(str(line)+"\n")
        w.close()
op.close()
