import sys
import os
from Bio.Seq import Seq
from itertools import islice
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import re
#sysa = sys.argv[1].split("/")
sysb = sys.argv[2]
def mergeIntervals(intervals):
    # Sort the array on the basis of start values of intervals.
    intervals.sort()
    stack = []
    # insert first interval into stack
    stack.append(intervals[0])
    for i in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)
 
    #print("The Merged Intervals are :", end=" ")
    for i in range(len(stack)):
        return stack[i]
 
 

w = open(sys.argv[3],"w")
handle = open(sys.argv[1],"r")
for record in SeqIO.parse(handle, "fasta") :
    id1 = record.id.split(":")
    id2 =id1[1].split("-")
    seq = str(record.seq) 
    k = 0
    t =len(seq)
    for i in range(1,t,1):
        str1 = seq[k: i]
        if len(str1)>0:
            list1 = []
            for d in re.finditer("[ATGCatgc]+",str1):
                list1.append([d.start(0),d.end(0)])
            if len(list1)>0:
                int1 = mergeIntervals(list1)
                str11 = re.sub("N|n","",str1)
                m =len(str11)
                if m == 0:
                    k = i
                if m == int(sysb):
                    #print("ok")
                #if m == 47:
                    gc = gc_fraction(str11,"remove")
                    int2 =[]
                    for s in range(len(int1)):
                        al = int(int1[s])+k+int(id2[0])
                        int2.append(al)
                    w.write("gc\t"+str(gc)+'\tseq\t'+str(str11)+"\t"+str(id2[0])+"\t"+str(id2[1])+"\t"+str(m)+"\t"+str(int2)+"\n")
                    k = i
        if len(str1) > 100000: 
             break
        

handle.close()
w.close()

