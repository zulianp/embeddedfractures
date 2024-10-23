import os
import json
import sys
seen = set()
sys.path = [path for path in sys.path if path not in seen and not seen.add(path)]
import utils.csv as csv_tools
from compute_mean_and_std_all import compute_mean_and_std

compute_mean_and_std_all = True
create_pdfs = True
copy_pdfs_to_overleaf = False

# Methods included in mean and standard deviation computation. focus_dir = methods_included[0] is currently not included
# in that computation. Once we are sure that USI/FEM_LM results are correct, we can include it.
methods_included = [
                    # "USI/FEM_LM",
                    # "USTUTT/MPFA",
                    # "UNICE_UNIGE/HFV_Cont",
                    "UNICAMP/Hybrid_Hdiv",
                    "UiB/TPFA",
                    "UiB/MPFA",
                    "UiB/MVEM",
                    "UiB/RT0"
]

focus_dir = methods_included[0]
focus_institute, focus_method = focus_dir.split("/")
focus_method = focus_method.replace("_", "\\_")
places_and_methods = {focus_institute: [focus_method], "mean": ["key"]}

def main():
    # Compute mean and standard deviation for all cases
    if compute_mean_and_std_all:
        print("Computing mean and standard deviations for all cases...")
        compute_mean_and_std(methods_included, focus_dir=focus_dir)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)
    places_and_methods_str = json.dumps(places_and_methods)  # Convert the dictionary to a JSON string
    for subdirectory in subdirectories:
        case = subdirectory.split(os.sep)[-1] # e.g. 1_single_fracture
        if case[0] in ["1", "2", "3", "4"]:
            if create_pdfs:
                print(f"Changing directory to {subdirectory} and running run_all.py there")
                os.system(f"cd {subdirectory} && python run_all.py '{places_and_methods_str}'")

    if copy_pdfs_to_overleaf:
        base_dir = "plots"
        subdirectories = csv_tools.find_direct_subdirectories(base_dir)
        for subdirectory in subdirectories:
            # List the files in subdirectory that contain the substring "combined"
            files = os.listdir(subdirectory)

            # Copy all files to ../overleaf_embedded_fractures/figures/pdf/
            for file in files:
                if file.endswith(".pdf"):
                    src = os.path.join(subdirectory, file)
                    dst = os.path.join("../overleaf_embedded_fractures/figures/pdf", file)
                    os.system(f"cp {src} {dst}")

if __name__ == "__main__":
    main()