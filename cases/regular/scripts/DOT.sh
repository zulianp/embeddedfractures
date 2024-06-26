#!/usr/bin/env bash

set -e

mkdir -p results
cd results
mkdir -p temp

cd ..

dirs=(small medium large) 
r=0


for d in ${dirs[@]}
do
	echo "DIR: $d"
	
	pvpython bench2_dot_block.py $d/matrix_transport.e results/temp/dot_cond1_block1.csv block_1
	pvpython bench2_dot_block.py $d/matrix_transport.e results/temp/dot_cond1_block2.csv block_2

	python3 bench2_dot_pandas.py results/temp/dot_cond1_block1.csv results/temp/dot_cond1_block2.csv results/dot_cond1_$r.csv
    r=$(($r + 1))

done

cd results
rm -r temp
cd ..
