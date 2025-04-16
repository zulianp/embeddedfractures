set -e

export results_dir=/Users/mariagiuseppinanestola/projects/parrot_2/utopia_with_trilinos/utopiatutorials/fracnetflow/3D/benchmarks/3 

echo "COPY PASTE FILES"

dirs=('small' 'medium' 'large') 

for d in ${dirs[@]}
do
	echo "DIR: $d"
	cp $results_dir/$d/fracture_flow.e small/
	cp $results_dir/$d/matrix_flow.e small/
	cp $results_dir/$d/fracture_transport.e small/
	cp $results_dir/$d/matrix_transport.e  small/
	cp $results_dir/$d/fracture_flow.e medium/
	cp $results_dir/$d/matrix_flow.e medium/
	cp $results_dir/$d/fracture_transport.e medium/
	cp $results_dir/$d/matrix_transport.e  medium/

done

echo "START ANALISYS"

./DOL.sh

./DOT.sh
