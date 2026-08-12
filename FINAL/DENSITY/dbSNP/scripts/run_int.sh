#!/bin/sh
for threshold in 39 40; do
     for suf in with no; do
 #   for control in control2_cleaned; do
    #    echo "Running: threshold=${threshold}"
        python intervals_110426_v8.py ${threshold} ${suf}
#        python intervals_110426_v8.py ${threshold}
done
done
