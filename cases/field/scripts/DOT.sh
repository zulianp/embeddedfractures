#!/usr/bin/env bash

set -e

mkdir -p results
cd results
mkdir -p temp

cd ..

dirs=(small medium large) 

r=0
block_start=1
block_end=52


for d in ${dirs[@]}
do
	echo "DIR: $d"
 
	for b in $(seq "$block_start" "$block_end"); 
	do
		pvpython bench2_dot_block.py $d/matrix_transport.e results/temp/dot_cond1_block$b.csv block_10
		b=$(($b + 1))
	done

	python3 bench2_dot_pandas.py results/temp/dot_cond1_block1.csv results/temp/dot_cond1_block2.csv results/dot_cond1_$r.csv
    r=$(($r + 1))

done

cd results
rm -r temp
cd ..
