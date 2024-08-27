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
	
	pvpython bench2_dol2.py $d/matrix_flow.e $d/matrix_transport.e results/temp/dol_swapped_col1.csv results/temp/dol_swapped_col2.csv results/temp/dol_swapped_col3.csv
	python3 bench2_dol_col.py results/temp/dol_swapped_col1.csv results/temp/dol_swapped_col2.csv results/temp/dol_swapped_col3.csv results/dol_cond1_$refinment.csv  $refinment
	
	echo $refinment

    refinment=$(($refinment + 1))

done

cd results
rm -r temp

cd ..