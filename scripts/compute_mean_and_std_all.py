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
    no_exceptions = True
    pattern_filename = f"dol_refinement_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 1 dol_refinement_*: {e}")
        no_exceptions = False
        pass

    pattern_filename = f"dot_refinement_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 1 dot_refinement_*: {e}")
        no_exceptions = False
        pass

    if no_exceptions:
        print("Processed case 1")


def process_case_2(subdirectory: str):
    no_exceptions = True
    pattern_filename = f"dol_cond_1_refinement_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 2 dol_cond_1_refinement_*: {e}")
        no_exceptions = False
        pass

    # NOTE: Waiting forArancia to fix the CSV files
    pattern_filename = f"dot_cond_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 2 dot_cond_*: {e}")
        no_exceptions = False
        pass

    if no_exceptions:
        print("Processed case 2")


def process_case_3(subdirectory: str):
    no_exceptions = True
    pattern_filename = f"dol_line_0_refinement_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 3 dol_line_0_refinement_*: {e}")
        no_exceptions = False
        pass

    pattern_filename = f"dol_line_1_refinement_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 3 dol_line_1_refinement_*: {e}")
        no_exceptions = False
        pass

    pattern_filename = f"dot_refinement_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 3 dot_refinement_*: {e}")
        no_exceptions = False
        pass

    # NOTE: Waiting forArancia to fix the CSV files
    pattern_filename = f"results.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 3 results.csv: {e}")
        no_exceptions = False
        pass

    if no_exceptions:
        print("Processed case 3")


def process_case_4(subdirectory: str):
    no_exceptions = True
    pattern_filename = f"dol_line_*.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 4 dol_line_*: {e}")
        no_exceptions = False
        pass

    pattern_filename = f"dot.csv"
    try:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory, pattern_filename=pattern_filename)
    except Exception as e:
        print(f"Error processing case 4 dot.csv: {e}")
        no_exceptions = False
        pass

    if no_exceptions:
        print("Processed case 4")

def main():
    print("Computing mean and standard deviations for all cases...")
    # Base directory in which to process CSV files
    base_dir = project_root + "/results"

    # Get all subdirectories of the base directory
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)

    for subdirectory in subdirectories:
        # Split based on os.path separator and get the last element
        case = subdirectory.split(os.sep)[-1]
        if "1" in case:
            process_case_1(subdirectory)
        elif "2" in case:
            process_case_2(subdirectory)
        elif "3" in case:
            process_case_3(subdirectory)
        elif "4" in case:
            process_case_4(subdirectory)
        else:
            raise ValueError("Invalid case name")

def test():
    base_dir = project_root + "/dummy_tests"
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)

    pattern_filename = f"results.csv"
    csv_tools.create_mean_and_std_csv_files(base_dir=base_dir, pattern_filename=pattern_filename)

if __name__ == "__main__":
    # test()
    main()

