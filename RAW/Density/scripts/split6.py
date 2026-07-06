import sys
#syssplit = sys.argv[1].split(".")
for i in range(1,25):
      op = open("../hg19_new_quadr_loop7_bed.bed","r")
      for line in op:
        line = line.strip()
        line2 = line.split()
        a = line2[0][3:]
        if a == str(i):
            w = open("../hg19_quadr/hg19_new_quadr_loop7_{}.bed".format(i),"a")
       #  w = open(str(syssplit[0])+"_{}".format(a)+".bed","a")
            w.write(str(line)+"\n")
            w.close()
      op.close()
