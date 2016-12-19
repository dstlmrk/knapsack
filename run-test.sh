#!/bin/bash

# for i in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
# for i in 030 060 090 120 150 180 210 240 270 300
for i in 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4 2.6 2.8
do
echo -ne $i "\t"
./knapsack.py --method all --path ../../knapgen/out/k/knap_inst_$i.dat --no-solution
done