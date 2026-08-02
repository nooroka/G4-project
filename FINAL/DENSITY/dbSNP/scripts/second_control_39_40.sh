#!/bin/bash
set -euo pipefail

mkdir -p ../control ../quadr ../quadr2

for j in {39..40}; do
    for i in {1..24}; do

        # --- quadr CG filtering ---
        python /data/nooroka/grant/punkt1/bioinformatics-cafe/fastaRegexFinder.py \
            -f /data/nooroka/grant/punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_${i}_${j}.fasta \
            -r '[Cc][Gg]' \
            > ../quadr/${i}_${j}_control3_CG_exclude.bed

        awk '{split($1, a, /[:\-]/); print a[1] "\t" a[2] "\t" a[3]}' \
            ../quadr/${i}_${j}_control3_CG_exclude.bed \
            | sort | uniq \
            > ../quadr/${i}_${j}_control3_CG_exclude_output.bed

        comm -23 \
            <(sort /data/nooroka/grant/punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_${i}_${j}.bed) \
            <(sort ../quadr/${i}_${j}_control3_CG_exclude_output.bed) \
            | bedtools sort \
            > ../quadr2/${i}_${j}_control3_cleaned.bed

        # --- control CG filtering ---
        INPUT_GZ="../control/gccoords_percents_${i}_my_${j}_control2_no_gc_corrected.txt.gz"
        OUTPUT_FASTA="../control/${i}_my_${j}_control2_no_gc_corrected_non_cleaned.fasta"
        OUTPUT_BED="../control/${i}_my_${j}_control2_no_gc_corrected_target_cleaned.bed"
        OUTPUT_CLEANED="../control/gccoords_percents_${i}_my_${j}_all_control2_no_gc_corrected_cleaned.txt"

        if [[ ! -f "$INPUT_GZ" ]]; then
            echo "File $INPUT_GZ not found, skipping."
            continue
        fi

        zcat "$INPUT_GZ" | python thres_to_fasta2.py - "$OUTPUT_FASTA"

        if [[ ! -f "$OUTPUT_FASTA" ]]; then
            echo "Can't make $OUTPUT_FASTA, skipping."
            continue
        fi

        python /data/nooroka/grant/punkt1/bioinformatics-cafe/fastaRegexFinder.py \
            -f "$OUTPUT_FASTA" \
            -r '[Cc][Gg]' \
            > "$OUTPUT_BED"

        zcat "$INPUT_GZ" | python target_line_numbers3_optimized_all.py - "$OUTPUT_BED" "$OUTPUT_CLEANED"

        echo "Completed ${j}, chr ${i}"
    done
done

echo "All files processed!"
