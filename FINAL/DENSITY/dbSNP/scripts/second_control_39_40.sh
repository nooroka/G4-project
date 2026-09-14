#!/bin/bash
set -euo pipefail
mkdir -p ../control ../quadr ../quadr2

has_with_not_without() {
    local name="$1"
    local stripped="${name//without/}"
    if [[ "$stripped" == *with* ]]; then
        return 0
    else
        return 1
    fi
}

MODES=("no_gc" "with_gc")

for j in {39..40}; do
    for i in {1..24}; do
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

        for MODE in "${MODES[@]}"; do
            GC_SUFFIX="${MODE}"
            INPUT_TXT="../control/gccoords_percents_${i}_my_${j}_control2_${GC_SUFFIX}.txt"
            OUTPUT_FASTA="../control/${i}_my_${j}_control2_${GC_SUFFIX}_non_cleaned.fasta"
            OUTPUT_BED="../control/${i}_my_${j}_control2_${GC_SUFFIX}_target_cleaned.bed"
            OUTPUT_CLEANED="../control/gccoords_percents_${i}_my_${j}_all_control2_${GC_SUFFIX}_cleaned.txt"

            if [[ ! -f "$INPUT_TXT" ]]; then
                echo "File $INPUT_TXT not found, skipping."
                continue
            fi

            python thres_to_fasta2.py "$INPUT_TXT" "$OUTPUT_FASTA"
            if [[ ! -f "$OUTPUT_FASTA" ]]; then
                echo "Can't make $OUTPUT_FASTA, skipping."
                continue
            fi

            python /data/nooroka/grant/punkt1/bioinformatics-cafe/fastaRegexFinder.py \
                -f "$OUTPUT_FASTA" \
                -r '[Cc][Gg]' \
                > "$OUTPUT_BED"

            python target_line_number_optimized_optimized.py "$INPUT_TXT" "$OUTPUT_BED" "$OUTPUT_CLEANED"

            if has_with_not_without "$MODE"; then
                if [ -f "$OUTPUT_CLEANED" ]; then
                    awk '$2 >= 0.5' "$OUTPUT_CLEANED" > "${OUTPUT_CLEANED}.tmp" && mv "${OUTPUT_CLEANED}.tmp" "$OUTPUT_CLEANED"
                    echo "Filter >= 0.5 applied to $OUTPUT_CLEANED (mode: ${MODE})"
                fi
            else
                echo "Filter skipped for mode ${MODE} (${OUTPUT_CLEANED})"
            fi

            echo "Completed ${j}, chr ${i}, mode ${MODE}"
        done
    done
done
echo "All files processed!"
