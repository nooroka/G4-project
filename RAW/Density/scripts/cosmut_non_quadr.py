#mutation density (COSMIC) for space between quadruplexes
import subprocess
import sys
w = open(sys.argv[4],"w")
def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count



d5 = count_lines_fast(sys.argv[2])
d1 = count_lines_fast(sys.argv[3])
d55=d5
d11=d1
op = open(sys.argv[1])

a  = ""
#if sys.argv[5] == '24':
 #   a =1
for line in op:
        line = line.strip()
        line = line.split()
        a = line[6]
op.close()
sum1 = int(d55)*int(a) #multiplying by interval length
    #w.write("chr{}".format(i)+"\t"+str(float(int(d11)/int(sum1)))+"\n")#mutation density
#if sys.argv[5] == '24':
 #   w.write("chr24"+"\t"+"0.0"+"\n")
#else:
if sum1 == 0:
    w.write("chr{}".format(sys.argv[5])+"\t"+"0.0"+"\n")
else:
    w.write("chr{}".format(sys.argv[5])+"\t"+str(float(int(d11)/int(sum1)))+"\n")
w.close()
