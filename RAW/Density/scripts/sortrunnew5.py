import sys
import os
for i in range(1,25,1):
    os.system("bedtools intersect -a  gccoords_all_genes{}_un.bed -b /data/nooroka/grant/punkt3/sort_sort_sort2/sort_sort_sort_sort2/bed/un/{}_2_sorted_un.bed > mutcosall{}.bed".format(i,i,i))
