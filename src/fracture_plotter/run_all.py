import importlib
import json
import os

seen = set()
import utils.csv as csv_tools

from fracture_plotter.utils.compute_mean_and_std_all import compute_mean_and_std
from fracture_plotter.utils.general import get_paths

compute_mean_and_std_all = True
create_pdfs = True
copy_pdfs_to_overleaf = False

# Methods included in mean and standard deviation computation.
methods_to_average = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]

CURRENT = True  # True for USI/FEM_LM, False for ETHZ_USI/FEM_LM
focus_dir = "USI/FEM_LM" if CURRENT else "ETHZ_USI/FEM_LM"
focus_institute, focus_method = focus_dir.split("/")
focus_method = focus_method.replace("_", "\\_")

places_and_methods = {focus_institute: [focus_method], "mean": ["key"]}


def main():
    paths = get_paths(__file__)

    # Compute mean and standard deviation for all cases, i.e. 1 (single fracture), 2 (regular fracture network), etc.
    if compute_mean_and_std_all:
        # Note: You may see some warnings in the interpolation code.
        print("Computing mean and standard deviations for all cases...")
        compute_mean_and_std(methods_to_average)

    subdirectories = csv_tools.find_direct_subdirectories(paths.module_dir)
    places_and_methods_str = json.dumps(
        places_and_methods
    )  # Convert the dictionary to a JSON string
    for subdirectory in subdirectories:
        case = subdirectory.split(os.sep)[-1]  # e.g. 1_single_fracture
        if case[0] in ["1", "2", "3", "4"]:
            if create_pdfs:
                print(
                    f"Changing directory to {subdirectory} and running run_all.py there"
                )
                os.system(
                    f"cd {os.path.join(subdirectory, 'visualization')} && python3 run_all.py '{places_and_methods_str}'"
                )

    if copy_pdfs_to_overleaf:
        subdirectories = csv_tools.find_direct_subdirectories(paths.plots_dir)
        for subdirectory in subdirectories:
            # List the files in subdirectory that contain the substring "combined"
            files = os.listdir(subdirectory)

            # Copy all files to ../overleaf_embedded_fractures/figures/pdf/
            for file in files:
                if file.endswith(".pdf"):
                    src = os.path.join(subdirectory, file)
                    dst = os.path.join("../overleaf_embedded_fractures/plots/", file)
                    os.system(f"cp {src} {dst}")


if __name__ == "__main__":
    main()
