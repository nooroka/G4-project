#!/bin/sh
for threshold in 39 40; do
    echo "Running: threshold=${threshold}"
    python intervals_out.py ${threshold}
done
