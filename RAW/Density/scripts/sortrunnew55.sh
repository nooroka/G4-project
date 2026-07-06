#!/bin/bash
#for i in {1..24}
#do
#	bedtools intersect -a  gccoords/gccoords_${i}_undefhg19.bed -b /data/nooroka/grant/punkt3/sort_sort_sort3/sort_sort_sort_sort3/bed/un/${i}_2_sorted_un.bed > mutcos40/mutcos_non_quadr${i}_40.bed #coordinates in mutation interquadruplex GC-rich file intersect with COSMIC mutation coordinates in all chromosomes
#done
bedtools intersect -a   <(awk 'BEGIN{OFS="\t"} { if ($3 <= $2) $3=$2+1; print }' $1) -b $2 -wa -wb > $3 #coordinates in mutation interquadruplex GC-rich file intersect with COSMIC mutation coordinates in all chromosomes
