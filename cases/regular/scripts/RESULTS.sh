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
	python3 results_pro.py $d/mesh_fracture.e $d/matrix_transport.e results/temp/results_cond1_ref$r.csv
    
    r=$(($r + 1))

done



tot_ref=${#dirs[@]}
python3 results_merge_rows.py results/results_cond1.csv  $tot_ref 'results/temp'

rm -r results/temp





# col=(3 4 5)

# HERE=$PWD
# r=0

# for d in ${dirs[@]}
# do
# 	echo "DIR: $d"
# 	ls $d
# 	cd $d

# 	pvpython $HERE/results_cond0_3.py mesh_fracture.e $HERE/mesh_results/results_cond0_3$r.csv
# 	pvpython $HERE/results_cond0_4.py matrix_flow.e $HERE/mesh_results/results_cond0_4$r.csv
#     pvpython $HERE/results_cond0_5.py matrix_flow.e $HERE/mesh_results/results_cond0_5$r.csv

# 	python3 $HERE/results_merge_col.py $HERE/mesh_results/results_cond0_3$r.csv $HERE/mesh_results/results_cond0_4$r.csv $HERE/mesh_results/results_cond0_5$r.csv $HERE/mesh_results/results_cond0_ref$r.csv 

# 	cd $HERE

#     r=$(($r + 1))

# done
# tot_ref=${#dirs[@]}
# python3 $HERE/results_merge_rows.py $HERE/mesh_results/results/results_cond0.csv  $tot_ref $HERE 

