import os
from percentiles import run_percentiles
from pol import run_pol
from pot import run_pot
from scripts.utils.general import get_paths, process_args
from scripts.utils.overlay import run_overlay
curr_dir = os.path.dirname(os.path.abspath(__file__))
case = curr_dir.split(os.sep)[-1]  # case we are dealing with
plots_dir, results_dir = get_paths(curr_dir)

def run_all():
    places_and_methods = process_args()
    print(f"Running all scripts in sequence for case {case}...")

    # run_percentiles(places_and_methods)
    # print("Finished running percentiles")

    run_pol(places_and_methods)
    print("Finished running pol")

    run_pot(places_and_methods)
    print("Finished running pot")

    files = [f"{curr_dir}/{case}_pol_c_fracture",
             f"{curr_dir}/{case}_pol_c_matrix",
             f"{curr_dir}/{case}_pol_p_matrix",
             f"{curr_dir}/{case}_pot_outflux"
             ]
    run_overlay(files, working_directory=curr_dir)
    print("Finished running overlay")

if __name__ == "__main__":
    run_all()
