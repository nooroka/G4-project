#!/bin/bash
for (( i=1; i<25; i++ ))
do
	python coords_gc_quadr.py ../../../punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_${i}_40.bed ../../../punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_${i}_40.fasta ../../../punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_${i}_gc_more_equal_50_40.bed ../../../punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_${i}_gc_more_equal_50_40.fasta
done
