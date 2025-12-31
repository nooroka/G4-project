#!/bin/sh
for file in /data/nooroka/grant/punkt3/stage2/hg19_quadr/merged/*.bed; do
    echo "Processing: $file"
    awk '{print $0, $3 - $2}' "$file" | sort -k4,4nr | tail -n 1
done
