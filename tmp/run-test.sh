#!/bin/bash

# for i in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
# for i in 030 060 090 120 150 180 210 240 270 300
# for i in 20 40 60 80 100 120 140 160 180 200
# for i in 0.45 0.50 0.55 0.60 0.70 0.75 0.80 0.85 0.90 0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99
for i in 200 400 600 800 1000 1200 1400 1600 1800 2000 2200 2400 2600 2800 3000 3200 3400 3600 3800 4000
do
./main.py --method sa --path ./data/inst/knap_40.inst.dat -i 100 -c 0.85 -t $i
done