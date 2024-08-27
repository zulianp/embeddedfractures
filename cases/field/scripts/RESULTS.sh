#!/usr/bin/env bash

# export PATH=../scripts:$PATH
# SCRIPT_PATH=$PWD/.. 

set -e
# set -x

#  benchmark_2
# |_ small
# 		|_ matrix_flow.e
#		|_ fracture_network.e
#		|_ ...
# |_ medium
# |_ large

# mkdir -p mesh_results
mkdir -p results
cd results
mkdir -p temp

cd ..

HERE=$PWD
r=0
dirs=('small' 'medium' 'large') 

for d in ${dirs[@]}
do
	echo "DIR: $d"
	python3 results_pro.py $d/mesh_fracture.e $d/matrix_transport.e results/temp/results_mesh_cond1_ref$r.csv
    pvpython results_inlet_pressure.py $d/matrix_flow.e results/temp/results_cond1_col9_ref$r.csv

    pvpython results_inlet_pressure.py $d/matrix_flow.e results/temp/results_cond1_col7_ref$r.csv
    pvpython results_inlet_pressure.py $d/matrix_flow.e results/temp/results_cond1_col8_ref$r.csv

    python3  results_merge_cols.py results/temp/results_mesh_cond1_ref$r.csv results/temp/results_cond1_col7_ref$r.csv results/temp/results_cond1_col8_ref$r.csv results/temp/results_cond1_col9_ref$r.csv results/temp/results_cond1_ref$r.csv
    r=$(($r + 1))

done



tot_ref=${#dirs[@]}
python3 results_merge_rows.py results/results_cond1.csv  $tot_ref 'results/temp'

rm -r results/temp





