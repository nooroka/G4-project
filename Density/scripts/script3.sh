#!/bin/bash
#for i in {1..24}
#do
#   awk '{{print $2,$3}}'  /data/nooroka/qgrs/comp${i}_out_gene_quadr_rev.txt >comp${i}_out_gene_quadr_rev1.bed
#   awk '{{print $2,$3}}' /data/nooroka/qgrs/comp${i}_out_gene_quadr.txt > comp_out_gene_quadr${i}.bed
#   sed -i 's/-/ /g' comp${i}_out_gene_quadr_rev1.bed
#   sed -i 's/-/ /g' comp_out_gene_quadr${i}.bed
#   awk '{{print $1"\t"$2-1"\t"$3}}' comp${i}_out_gene_quadr_rev1.bed > comp${i}_out_gene_quadr_rev11.bed
#   awk '{{print $1"\t"$3-1"\t"$2}}' comp${i}_out_gene_quadr_rev1.bed > comp${i}_out_gene_quadr_rev111.bed
#   sort -nk 2,3  comp${i}_out_gene_quadr_rev111.bed >  comp${i}_out_gene_quadr_rev111_sorted.bed
#   awk '{{print $1"\t"$2"\t"$3}}' comp_out_gene_quadr${i}.bed > comp_out_gene_quadr${i}${i}.bed
#   cat  comp${i}_out_gene_quadr_rev111_sorted.bed  comp_out_gene_quadr${i}${i}.bed > comp${i}_out_gene_quadr_all.bed
#   sort -nk2,3 comp${i}_out_gene_quadr_all.bed > comp${i}_out_gene_quadr_all_sorted.bed
samtools faidx $1
#done
