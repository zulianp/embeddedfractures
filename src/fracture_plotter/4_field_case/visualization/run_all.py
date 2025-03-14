import json
import os
import sys

# from percentiles import run_percentiles
from pol import run_pol
from pot import run_pot

from fracture_plotter.utils.general import get_paths, process_args
from fracture_plotter.utils.overlay import run_overlay


def run_all():
    paths = get_paths(__file__)

    places_and_methods = process_args()
    print(f"Running all scripts in sequence for case {paths.case}...")

    # run_percentiles(places_and_methods)
    # print("Finished running percentiles")

    run_pol(places_and_methods)
    print("Finished running pol")

    run_pot(places_and_methods)
    print("Finished running pot")

    files = [
        os.path.join(paths.tex_dir, f"{paths.case}_pol_line_1"),
        os.path.join(paths.tex_dir, f"{paths.case}_pol_line_2"),
        os.path.join(paths.tex_dir, f"{paths.case}_pot"),
    ]

    run_overlay(files, paths)
    print("Finished running overlay")


if __name__ == "__main__":
    run_all()
