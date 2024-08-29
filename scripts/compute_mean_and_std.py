### Imports ###
import os
import sys
import pandas as pd
import numpy as np

# Ensure the working directory is the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import scripts.utils.csv as csv_tools
################

def process_case_1(subdirectory: str):
    pattern_filename = f"dol_refinement_*.csv"
    csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)

    pattern_filename = f"dot_refinement_*.csv"
    csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)

def main():
    # Base directory in which to process CSV files
    base_dir = project_root + "/results"

    # Get all subdirectories of the base directory
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)

    for subdirectory in subdirectories:
        # Split based on os.path separator and get the last element
        case = subdirectory.split(os.sep)[-1]
        if "1" in case:
            process_case_1(subdirectory)
        # elif "2" in case:
        #     print("Hello")
        # elif "3" in case:
        #     print("Salut")
        # elif "4" in case:
        #     print("Hola")
        # else:
        #     raise ValueError("Invalid case name")

def test():
    base_dir = project_root + "/dummy_tests"
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)

    pattern_filename = f"results.csv"
    csv_tools.create_mean_and_std_csv_files(base_dir=base_dir, pattern_filename=pattern_filename)

if __name__ == "__main__":
    # test()
    main()

