# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
from pol import run_pol
from pot import run_pot
from scripts.utils.overlay import run_overlay

def run_all():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    print(f"Running all scripts in sequence for case {case}...")

    run_pol()
    print("Finished running pol")

    run_pot()
    print("Finished running pot")

    files = [f"{case}_pol_cond_1",
             "overlay_fig2"
             ]
    run_overlay(files, working_directory=curr_dir)
    print("Finished running overlay")


if __name__ == "__main__":
    run_all()
