#!/bin/bash
#set -euo pipefail

run_iteration() {
    t=$1
    i=$2

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

process_filtering() {
    t=$1
    i=$2
    input_file="../input_loop7_${t}.txt"

    if [ ! -f "$input_file" ]; then
        echo "File $input_file does not exist."
        exit 1
    fi

    j=$(awk -v chr="$i" '$1 == chr {print $2}' "$input_file")

    if [[ -z "$j" ]]; then
        echo "No entry for chr ${i} in ${input_file}. Skipping."
        return
    fi

    input_filename="../control/gccoords_percents_${i}_my_${t}_all_control3_no_gc.txt"
    output_filename="../filtered2/max_all_${t}_${i}_control3_no_gc.txt"

    if [ ! -f "$input_filename" ]; then
        echo "File $input_filename does not exist. Skipping (${i}, ${j})."
        return
    fi

    sort -nk2 -r "$input_filename" | head -n "$j" > "$output_filename"
    echo "Processed (${i}, ${j}). Result saved to $output_filename."
}

for t in 39 40; do
    echo "=== Running pipeline for threshold ${t} ==="
    for i in $(seq 1 24); do
        run_iteration ${t} ${i}
    done
    echo "=== Pipeline for threshold ${t} completed ==="

    echo "=== Running filtering for threshold ${t} ==="
    for i in $(seq 1 24); do
        process_filtering ${t} ${i} 
    done
    echo "=== Filtering for threshold ${t} completed ==="
done
