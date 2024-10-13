# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
from pol import run_pol
from pot import run_pot
from scripts.utils.overlay import run_overlay
from plotroutines import get_paths

def run_all():
    curr_dir, plots_dir, results_dir, utils_dir = get_paths()
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    print(f"Running all scripts in sequence for case {case}...")

    run_pol()
    print("Finished running pol")

    # run_boundary_data()
    # print("Finished running boundary data")

    run_pot()
    print("Finished running pot")

    files = [f"{curr_dir}/{case}_pol_p_line_0",
             f"{curr_dir}/{case}_pot_fracture_3"
             ]
    run_overlay(files, working_directory=curr_dir)
    print("Finished running overlay")


if __name__ == '__main__':
    run_all()