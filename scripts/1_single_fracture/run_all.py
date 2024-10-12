import os
from percentiles import run_percentiles
from pol import run_pol
from pot import run_pot
from plotroutines import get_paths

def run_all():
    curr_dir, plots_dir, results_dir, utils_dir = get_paths()
    case = curr_dir.split(os.sep)[-1]  # case we are dealing with
    print(f"Running all scripts in sequence for case {case}...")

    run_percentiles()
    print("Finished running percentiles")

    run_pol()
    print("Finished running pol")

    run_pot()
    print("Finished running pot")

if __name__ == "__main__":
    run_all()
