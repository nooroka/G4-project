import os
import sys
def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num
#for i in range(1,25,1):
op = open(sys.argv[1],"r")
for line in op:
        line = line.strip()
        line = line.split()
        line11 = int_r(float(line[1]))
        if int(line[0][3:])==int(sys.argv[4]):
            a = line11
os.system("python ../scripts/windowcoords13.py {} {} {}".format(sys.argv[2],a,sys.argv[3]))
op.close()
