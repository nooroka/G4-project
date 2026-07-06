#!/bin/bash

run_iteration() {
    t=$1   # threshold: 39 or 40
    i=$2   # iteration number: 1..24

    # --- Step 1: G4 filtering ---
    python thres_to_fasta.py \
        <(zcat ../control/gccoords_percents_${i}_my_${t}_control2_no_gc.txt.gz) \
        ../control/${i}_${t}_all_loop7_no_gc.fasta

    python /data/nooroka/grant/punkt1/bioinformatics-cafe/fastaRegexFinder.py \
        -f ../control/${i}_${t}_all_loop7_no_gc.fasta \
        -r '[gG]{3,}\w{1,7}[gG]{3,}\w{1,7}[gG]{3,}\w{1,7}[gG]{3,}' \
        > ../control/${i}_${t}_all_loop7_no_gc.bed

    python target_line_numbers.py \
        <(zcat ../control/gccoords_percents_${i}_my_${t}_control2_no_gc.txt.gz) \
        ../control/${i}_${t}_all_loop7_no_gc.bed \
        ../control/gccoords_percents_${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_no_gc.txt

    # --- Step 2: CG filtering ---
    python thres_to_fasta.py \
        ../control/gccoords_percents_${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_no_gc.txt \
        ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_no_gc.fasta

    python /data/nooroka/grant/punkt1/bioinformatics-cafe/fastaRegexFinder.py \
        -f ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_no_gc.fasta \
        -r '[Cc][Gg]' \
        > ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_target_no_gc.bed

    python target_line_numbers_optimized_all.py \
        ../control/gccoords_percents_${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_no_gc.txt \
        ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_target_no_gc.bed \
        ../control/gccoords_percents_${i}_my_${t}_all_control3_no_gc.txt

    echo "Threshold ${t}, iteration ${i} completed"
}
export -f run_iteration

for t in 39 40; do
    echo "=== Running for threshold ${t} ==="
    seq 1 24 | parallel -j 1 run_iteration ${t} {}
    echo "=== Threshold ${t} completed ==="
done

echo "All iterations completed"
