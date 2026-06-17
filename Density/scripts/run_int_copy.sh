#!/bin/sh
for threshold in 39 40;  do
 #   for control in control2; do
       # echo "Running: threshold=${threshold} control1=${control}"
        python intervals_110426_v8_copy.py ${threshold} ${control}
       # python intervals_110426_v8.py ${threshold} 
  #  done
done
