#mutational density for COSMIC
import subprocess
import sys
w = open(sys.argv[3],"w")
#w = open("mutdensgene_quadr40.txt","a")
#for i in range(1,25,1):
op = open(sys.argv[1],"r")
    #op = open("../punkt1/merged/quadr7_chain180424_merged2_sorted_{}_40.bed".format(i),"r")
sum1 = 0
for line in op:
        line = line.strip()
        line = line.split()
        sum22=int(line[2])-int(line[1]) #interval length for the all genome, except genes
        sum1+=sum22
op.close()  
#d1 = subprocess.check_output("wc -l {}".format(sys.argv[2]),shell = True) #число мутаций на длину квадруплекса
def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count
#d1 = subprocess.check_output('wc -l mutcos40/mutcosquadr{}_40.bed'.format(i),shell = True)#number of mutations
#d11 = d1.decode().split()[0]
d1 = count_lines_fast(sys.argv[2])
d11 = d1
if sum1==0:
    w.write("chr{}".format(sys.argv[4])+"\t"+"0"+"\n")
else:
    w.write("chr{}".format(sys.argv[4])+"\t"+str(float(int(d11)/int(sum1)))+"\n")#  
#w.write("chr{}".format(i)+"\t"+str(float(int(d11)/int(sum1)))+"\n")#density calculation
#w.close(a)
