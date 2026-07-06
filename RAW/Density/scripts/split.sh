for i in {1..24}
do
    bedtools subtract -a ../../hg19/hg19_new${i}.fna.bed  -b /data/nooroka/grant/punkt3/stage2/gccoords/hg19/${i}_hg19_control3_cleaned.bed > ../compgene/hg19_non_quadr_gc_cleaned_${i}.bed
done
