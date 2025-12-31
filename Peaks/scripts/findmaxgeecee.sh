#!/bin/bash

# Directory containing your files
FILES_DIR="/data/nooroka/grant/punkt1/stage2/geecee"

# Function to find the maximum value in the second column of a file
# Function to find the maximum value in the second column of a file, skipping the first line
find_max_in_file() {
  local file=$1
  awk 'NR > 1 { if ($2 > max) max = $2 } END { print max }' max=-inf "$file"
}

# Loop over each file in the directory matching the pattern *loop5*geecee*
for file in "$FILES_DIR"/quadr7_*_extracted.geecee; do
  if [[ -f $file ]]; then
    echo "Processing file: $file"
    max_value=$(find_max_in_file "$file")
    echo "Maximum value in second column of $file: $max_value"
  fi
done
