import os
import sys
seen = set()
sys.path = [path for path in sys.path if path not in seen and not seen.add(path)]
import utils.csv as csv_tools
from compute_mean_and_std_all import compute_mean_and_std

compute_mean_and_std_all = False
create_pdfs = True
copy_pdfs_to_overleaf = False

methods_included = ["USI/FEM_LM",
                    "USTUTT/MPFA",
                    "UiB/TPFA",
                    "UiB/MPFA",
                    "UiB/MVEM",
                    "UiB/RT0"]

def main():
    # Compute mean and standard deviation for all cases
    if compute_mean_and_std_all:
        print("Computing mean and standard deviations for all cases...")
        compute_mean_and_std(methods_included)

    if create_pdfs:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        subdirectories = csv_tools.find_direct_subdirectories(base_dir)
        for subdirectory in subdirectories:
                case = subdirectory.split(os.sep)[-1] # e.g. 1_single_fracture
                if case[0] in ["1"]:#["1", "2", "3", "4"]:
                    print(f"Changing directory to {subdirectory}")
                    os.system(f"cd {subdirectory} && python run_all.py")

                    plots_directory = os.path.join('plots', subdirectory).replace("scripts", "plots")
                    # os.system(f"python combine_pdfs.py {plots_directory}")

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