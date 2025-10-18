#!/bin/bash
#for i in {1..24}
#do
#bedtools intersect -a  ../punkt1/merged/quadr7_chain180424_merged2_sorted_${i}.bed -b /data/nooroka/grant/punkt3/sort_sort_sort3/sort_sort_sort_sort3/bed/un/${i}_2_sorted_un.bed > mutcos39/mutcosquadr${i}_39.bed #coordinates in mutation quadruplex  file intersect with COSMIC mutation coordinates in all chromosomes
#done
bedtools intersect -a  $1 -b $2 | bedtools sort | bedtools merge  > $3 #coordinates in mutation quadruplex  file intersect with COSMIC mutation coordinates in all chromosomes
#
