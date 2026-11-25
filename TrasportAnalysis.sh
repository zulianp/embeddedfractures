#!/usr/bin/env bash

# export PATH=../scripts:$PATH
# SCRIPT_PATH=$PWD/.. 

#!/bin/bash

set -e

export HOME_DIR="/Users/mariagiuseppinanestola/Unidstance/embeddedfractures"

BASE_DIR="/Users/mariagiuseppinanestola/Unidstance/embeddedfractures/src/fracture_plotter"

dirs=(single_fracture regular_fracture small_feature field_case)


for d in "${dirs[@]}"; do
    echo "DIR: $d"

    cd "$BASE_DIR/$d/postprocessing"

    ./DOL.sh
    ./DOT.sh

    cp results/* "$HOME_DIR/results/$d/USI/FEM_LM"
done

cd "$HOME_DIR"

python3.12 main.py 
