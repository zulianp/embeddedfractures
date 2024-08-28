### Imports ###
import os
import sys
import pandas as pd
import numpy as np

# Ensure the working directory is the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
import scripts.utils.csv as csv_tools
################

# Base directory is results + the name of this file's parent directory
base_dir = csv_tools.get_base_dir(project_root=project_root, file_dirname=os.path.dirname(__file__))

refinement_indices = [0, 1, 2]
for ref in refinement_indices:
    # Create mean and standard deviation CSV files taking into account all filenames with filename in any subdirectory of base_dir
    filename_dol = f"dol_refinement_{ref}.csv"
    csv_tools.create_mean_and_std_csv_files(base_dir=base_dir, filename=filename_dol, reference_column="arc_length")

    filename_dot = f"dot_refinement_{ref}.csv"
    csv_tools.create_mean_and_std_csv_files(base_dir=base_dir, filename=filename_dot, reference_column="arc_length")




