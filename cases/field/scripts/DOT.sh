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

	for b in {1..52}
	do 
		echo "$b"
		pvpython bench2_dot_block.py $d/fracture_transport.e results/temp/dot_cond1_block$b.csv $b

		if [ "$b" = 1 ]; 
		 then
		 	echo "primo giro"

		elif [ "$b" -gt 1 -a "$b" -le 51 ]
		 then

		 	let "bb = $b - 1"
			echo "$bb"
		    python3 bench2_dot_pandas.py results/temp/dot_cond1_block$bb.csv results/temp/dot_cond1_block$b.csv results/temp/dot_cond1_block$b.csv $b
		
		else 
			let "bb = $b - 1"
		    python3 bench2_dot_pandas.py results/temp/dot_cond1_block$bb.csv results/temp/dot_cond1_block$b.csv results/dot_cond1_$r.csv $b

		fi
    done 

    r=$(($r + 1))

done

cd results
rm -r temp
cd ..
