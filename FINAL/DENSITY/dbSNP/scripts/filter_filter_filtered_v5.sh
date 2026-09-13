#!/bin/bash
#set -euo pipefail

# Проверяет, содержит ли имя файла "with", но не как часть слова "without"
has_with_not_without() {
    local name="$1"
    local stripped="${name//without/}"
    if [[ "$stripped" == *with* ]]; then
        return 0
    else
        return 1
    fi
}

run_iteration() {
    t=$1
    i=$2
    gc=$3
    python thres_to_fasta.py \
        ../control/gccoords_percents_${i}_my_${t}_control_${gc}.txt \
        ../control/${i}_${t}_all_loop7_${gc}.fasta
    python /data/nooroka/grant/punkt1/bioinformatics-cafe/fastaRegexFinder.py \
        -f ../control/${i}_${t}_all_loop7_${gc}.fasta \
        -r '[gG]{3,}\w{1,7}[gG]{3,}\w{1,7}[gG]{3,}\w{1,7}[gG]{3,}' \
        > ../control/${i}_${t}_all_loop7_${gc}.bed
    python target_line_numbers_optimized_all.py \
        ../control/gccoords_percents_${i}_my_${t}_control2_${gc}.txt  \
        ../control/${i}_${t}_all_loop7_${gc}.bed \
        ../control/gccoords_percents_${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_${gc}.txt
    python thres_to_fasta.py \
        ../control/gccoords_percents_${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_${gc}.txt \
        ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_${gc}.fasta
    python /data/nooroka/grant/punkt1/bioinformatics-cafe/fastaRegexFinder.py \
        -f ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_${gc}.fasta \
        -r '[Cc][Gg]' \
        > ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_target_${gc}.bed
    python target_line_numbers_optimized_all.py \
        ../control/gccoords_percents_${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_${gc}.txt \
        ../control/${i}_my_${t}_subtract_from_all_filtered_without_quadr_loop7_target_${gc}.bed \
        ../control/gccoords_percents_${i}_my_${t}_all_control3_${gc}.txt

    # ── ограничение: вторая колонка >= 0.5, только если в имени файла есть "with" (не "without") ──
    control3_file="../control/gccoords_percents_${i}_my_${t}_all_control3_${gc}.txt"
    if [ -f "$control3_file" ]; then
        if has_with_not_without "$control3_file"; then
            awk '$2 >= 0.5' "$control3_file" > "${control3_file}.tmp" && mv "${control3_file}.tmp" "$control3_file"
            echo "Filter >= 0.5 applied to $control3_file (contains 'with')"
        else
            echo "Filter skipped for $control3_file (no standalone 'with' in name)"
        fi
    fi

    echo "Threshold ${t}, iteration ${i}, gc=${gc} completed"
}

process_filtering() {
    t=$1
    i=$2
    gc=$3
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
    input_filename="../control/gccoords_percents_${i}_my_${t}_all_control3_${gc}.txt"
    output_filename="../filtered2/max_all_${t}_${i}_control3_${gc}.txt"
    if [ ! -f "$input_filename" ]; then
        echo "File $input_filename does not exist. Skipping (${i}, ${j})."
        return
    fi
    sort -nk2 -r "$input_filename" | head -n "$j" > "$output_filename"
    echo "Processed (${i}, ${j}, gc=${gc}). Result saved to $output_filename."
}

for gc in no_gc with_gc; do
    echo "##### Running for gc variant: ${gc} #####"
    for t in 39 40; do
        echo "=== Running pipeline for threshold ${t}, gc=${gc} ==="
        for i in $(seq 1 24); do
            run_iteration ${t} ${i} ${gc}
        done
        echo "=== Pipeline for threshold ${t}, gc=${gc} completed ==="
        echo "=== Running filtering for threshold ${t}, gc=${gc} ==="
        for i in $(seq 1 24); do
            process_filtering ${t} ${i} ${gc}
        done
        echo "=== Filtering for threshold ${t}, gc=${gc} completed ==="
    done
done
