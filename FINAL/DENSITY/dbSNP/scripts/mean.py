import subprocess
from statistics import mean
import sys
sum2 = 0
op = open(sys.argv[1],"r")
sum1 = 0
for line in op:
        line = line.strip()
        line = line.split()
        mean1 = int(line[2])-int(line[1])
        print(line, mean1)
        sum1+=mean1
d6 = subprocess.check_output('wc -l {}'.format(sys.argv[1]),shell = True)
d6 = d6.decode().split()[0]
    #print(d6)
del1 = int(sum1)/int(d6)
w = open(sys.argv[2],"w")
#for k in range(len(list1)):
sysa = sys.argv[1].split("_")
sysb = sysa[-3]
w.write("chr" + str(str(sysb))+"\t"+str(del1)+"\n")
w.close()


