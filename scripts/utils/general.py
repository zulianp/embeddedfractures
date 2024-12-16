import sys
import json
import os

def process_args():
    if len(sys.argv) > 1:
        # Get the argument passed for places_and_methods
        places_and_methods_str = sys.argv[1]
        places_and_methods = json.loads(places_and_methods_str)  # Convert JSON string back to dictionary
        print("Received places_and_methods:", places_and_methods)
    else:
        places_and_methods = {"USI": ["FEM\_LM"], "mean": ["key"]}
        print(f"No places_and_methods passed. Setting default to {places_and_methods}")
    return places_and_methods

def get_paths(curr_dir):
    plots_dir = curr_dir.replace('scripts', 'plots')
    results_dir = curr_dir.replace('scripts', 'results')
    return plots_dir, results_dir