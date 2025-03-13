import json
import os
import sys
from types import SimpleNamespace


def process_args():
    if len(sys.argv) > 1:
        # Get the argument passed for places_and_methods
        places_and_methods_str = sys.argv[1]
        places_and_methods = json.loads(
            places_and_methods_str
        )  # Convert JSON string back to dictionary
        print("Received places_and_methods:", places_and_methods)
    else:
        places_and_methods = {"USI": ["FEM\_LM"], "mean": ["key"]}
        print(f"No places_and_methods passed. Setting default to {places_and_methods}")
    return places_and_methods


def get_paths(file_handle, package_dir="src/fracture_plotter"):
    curr_dir = os.path.dirname(os.path.abspath(file_handle))
    tex_dir = os.path.join(os.path.dirname(curr_dir), "tex_files")
    tex_figs_dir = os.path.join(os.path.dirname(curr_dir), "figures")
    case = curr_dir.split(os.sep)[-2]
    plots_dir = os.path.dirname(curr_dir).replace(package_dir, "plots")
    results_dir = os.path.dirname(curr_dir).replace(package_dir, "results")
    return SimpleNamespace(
        curr_dir=curr_dir,
        case=case,
        plots_dir=plots_dir,
        results_dir=results_dir,
        tex_dir=tex_dir,
        tex_figs_dir=tex_figs_dir,
    )
