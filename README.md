# Project Structure

The project directory is organized as follows:
- `plots`
- `results`
- `scripts`

Each of the above folders contains four subfolders, corresponding to specific cases:

- `1_single_fracture/`
- `2_regular_fracture_network/`
- `3_network_with_small_features/`
- `4_field_case/`

The case subfolders across `plots`, `results`, and `scripts` are aligned with one another, meaning that they contain files corresponding to the same case.

## `scripts` Folder

The `scripts/` folder contains Python files essential for processing and analyzing the data. Notably:

- **`compute_mean_and_std_all.py`**: This script computes the mean and standard deviation for results stored in CSV files across different institutions, with a focus on the `USI/FEM_LM` results.
  
- **`run_all.py`**: This script automates the execution of all necessary Python scripts and copies the generated figures directly into the Overleaf folder containing the project data. It assumes that both the project folder and the Overleaf folder share the same parent directory.

