import os
import sys
import argparse

# Ensure the working directory is the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import scripts.utils.csv as csv_tools

def process_patterns(subdirectory: str, patterns: list, case_id: str, methods_included: list[str]):
    no_exceptions = True

    for pattern_filename in patterns:
        csv_tools.create_mean_and_std_csv_files(base_dir=subdirectory,
                                                pattern_filename=pattern_filename,
                                                methods_included=methods_included)
        print(f"Processed {case_id}")

def compute_mean_and_std(methods_included):
    if type(methods_included) == str:
        methods_included = methods_included.split(',')  # Split the comma-separated string into a list

    # Base directory in which to process CSV files
    base_dir = project_root + "/results"

    # Define a dictionary mapping case identifiers to pattern lists
    case_patterns = {
        "1": [
            "dol_refinement_*.csv",
            "dot_refinement_*.csv"
        ],
        "2": [
            "dol_cond_0_refinement_*.csv",
            "dot_cond_*.csv"  # NOTE: Waiting for Arancia to fix the CSV files
        ],
        "3": [
            "dol_line_0_refinement_*.csv",
            "dol_line_1_refinement_*.csv",
            "dot_refinement_*.csv",
            "results.csv"  # NOTE: Waiting for Arancia to fix the CSV files
        ],
        "4": [
            "dol_line_*.csv",
            "dot.csv"
        ]
    }

    # Get all subdirectories of the base directory
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)

    for subdirectory in subdirectories:
        # Split based on os.path separator and get the last element
        case = subdirectory.split(os.sep)[-1]

        # Find patterns based on case identifier using the dictionary
        for key in case_patterns:
            if key in case:
                patterns = case_patterns[key]
                process_patterns(subdirectory, patterns, case, methods_included=methods_included)
                break
        else:
            raise ValueError(f"Invalid case name: {case}")


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process patterns with optional methods.")
    parser.add_argument('--methods_included', type=str, required=False, default=None,
                        help="Specify methods to include.")

    # Parse arguments
    args = parser.parse_args()

    # Call main with parsed methods_included argument
    args.methods_included = ["USI/FEM_LM", "USTUTT/MPFA", "UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]
    args.methods_included = ",".join(args.methods_included)
    compute_mean_and_std(args.methods_included)
