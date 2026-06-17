#!/bin/sh
for threshold in 39 40; do
 #   for control in control2_cleaned; do
        echo "Running: threshold=${threshold}"
       # python intervals_110426_v8.py ${threshold} ${control}
        python intervals_110426_v8.py ${threshold} 
   # done
done
