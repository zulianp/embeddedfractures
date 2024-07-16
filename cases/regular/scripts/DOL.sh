#!/usr/bin/env bash

# export PATH=../scripts:$PATH
# SCRIPT_PATH=$PWD/.. 

set -e

mkdir -p results
cd results
mkdir -p temp

cd ..

dirs=(small medium large) 


refinment=0

for d in ${dirs[@]}
do
	echo "DIR: $d"
	
	pvpython bench2_dol.py $d/matrix_flow.e results/temp/dol_swapped.csv
	python3 bench2_dol_swap_col_0.py results/temp/dol_swapped.csv results/dol_cond1_$refinment.csv  $refinment
	
	echo $refinment

    refinment=$(($refinment + 1))

done

cd results
rm -r temp

cd ..