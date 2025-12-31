#mutation density (COSMIC) for space between quadruplexes
import subprocess
import sys
#w = open("mutdensgene_non_quadr40.txt","a")
w = open(sys.argv[4],"w")
#for i in range(1,25,1):
#    d5 = subprocess.check_output("wc -l gccoords/gccoords_{}_undefhg19.bed".format(i),shell = True)  
d5 = subprocess.check_output("wc -l {}".format(sys.argv[2]),shell = True)
    #d1 = subprocess.check_output('wc -l mutcos40/mutcos_non_quadr{}.bed'.format(i),shell = True)#number of mutations
d1 = subprocess.check_output("wc -l {}".format(sys.argv[3]),shell = True)
d55 = d5.decode().split()[0]
d11 = d1.decode().split()[0]
   # op = open("gccoords/gccoords_percents_{}_my_40.txt".format(i),"r")
op = open(sys.argv[1])
a  = ""
for line in op:
        line = line.strip()
        line = line.split()
        a = line[6]
op.close()
sum1 = int(d55)*int(a) #multiplying by interval length
    #w.write("chr{}".format(i)+"\t"+str(float(int(d11)/int(sum1)))+"\n")#mutation density
w.write("chr{}".format(sys.argv[5])+"\t"+str(float(int(d11)/int(sum1)))+"\n")
w.close()
