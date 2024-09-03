#!/usr/bin/env bash

set -e

mkdir -p results
cd results
mkdir -p temp

cd ..

dirs=( medium ) 
r=0


for d in ${dirs[@]}
do
	echo "DIR: $d"
	
	pvpython bench2_dot_blockid1_10_11.py $d/matrix_transport.e results/temp/dot_cond1_block1.csv results/temp/dot_cond1_block10.csv results/temp/dot_cond1_block11.csv

	python3 bench2_dot_pandas.py results/temp/dot_cond1_block1.csv results/temp/dot_cond1_block10.csv results/temp/dot_cond1_block11.csv results/dot_cond1.csv
    r=$(($r + 1))

done

cd results
rm -r temp
cd ..
