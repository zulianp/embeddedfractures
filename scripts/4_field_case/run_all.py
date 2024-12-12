import os
import sys
import json
from percentiles import run_percentiles
from pol import run_pol
from pot import run_pot
from scripts.utils.overlay import run_overlay
from plotroutines import get_paths

def run_all():
    # Get the argument passed for places_and_methods
    if len(sys.argv) > 1:
        places_and_methods_str = sys.argv[1]
        places_and_methods = json.loads(places_and_methods_str)  # Convert JSON string back to dictionary
        print("Received places_and_methods:", places_and_methods)
    else:
        places_and_methods = {"USI": ["FEM\_LM"], "mean": ["key"]}
        print(f"No places_and_methods passed. Setting default to {places_and_methods}")

    curr_dir, plots_dir, results_dir, utils_dir = get_paths()
    case = curr_dir.split(os.sep)[-1]  # case we are dealing with
    print(f"Running all scripts in sequence for case {case}...")

    # run_percentiles(places_and_methods)
    # print("Finished running percentiles")

    run_pol(places_and_methods)
    print("Finished running pol")

    run_pot(places_and_methods)
    print("Finished running pot")

    files = [f"{case}_pol_line_1",
             f"{case}_pol_line_2",
             f"{case}_pot"]

    run_overlay(files, working_directory=curr_dir)
    print("Finished running overlay")


if __name__ == "__main__":
    run_all()
