# Project Structure

The project directory is organized as follows:

- `plots` (created automatically for you)
- `results`
- `src/fracture_plotter` (this is the module)

Each of the above folders contains four subfolders in common, corresponding to the following cases:

- `single_fracture/`
- `regular_fracture/`
- `small_features/`
- `field_case/`

## Module Folder

The `src/fracture_plotter/utils` folder contains Python files essential for processing and analyzing the data. Notably:

- **`compute_mean_and_std_all.py`**: This script computes the mean and standard deviation for results stored in CSV files across different institutions, with a focus on the `USI/FEM_LM` results.
- **`run_all.py`**: This script automates the execution of all necessary Python scripts and copies the generated figures directly into the Overleaf folder containing the project data. It assumes that both the project folder and the Overleaf folder share the same parent directory.
