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
	
	pvpython bench2_dot_col12.py $d/matrix_transport.e results/temp/dot_cond1_col1.csv results/temp/dot_cond1_col2.csv 
	pvpython bench2_dot_col3.py $d/matrix_transport.e results/temp/dot_cond1_col3.csv 

	python3 bench2_dot_pandas.py results/temp/dot_cond1_col1.csv results/temp/dot_cond1_col2.csv results/temp/dot_cond1_col3.csv results/dot_refinement_$r.csv
    r=$(($r + 1))

done

cd results
rm -r temp
cd ..
