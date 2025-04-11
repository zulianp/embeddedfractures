# Fracture Plotter

## Installation
```bash
./setup_venv.sh
```
**Note:** This script sets up a Python virtual environment and installs the package in editable mode.

## Usage
```bash
source venv/bin/activate
python3 main.py
```
**Note:** Modify the parameters in `main.py` as needed.

## Project Structure

```
.
├── plots/           # Automatically created for storing generated plots
├── results/         # CSV files (results from all institutions/methods)
└── src/
    └── fracture_plotter/  # Main module for visualizing results
```

Each of the main folders (`plots`, `results`, and `fracture_plotter`) contains the following subfolders:
- `single_fracture`
- `regular_fracture`
- `small_features`
- `field_case`

## Some Comments
In the visualization code, "pol" stands for "plot over line" and "pot" stands for "plot over time", following the same naming scheme from the original paper: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d