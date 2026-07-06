#!/bin/bash
for i in {1..24}
do
    bedtools merge -i ../hg19_quadr/hg19_new_quadr_loop7_${i}.bed > ../hg19_quadr/merged/hg19_new_quadr_loop7_merged_${i}.bed 
done

