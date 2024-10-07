import os 
import utils.csv as csv_tools

compute_mean_and_std_all = True
create_pdfs = True
copy_pdfs_to_overleaf = False

def main():
    if compute_mean_and_std_all:
        # Compute mean and standard deviation for all cases
        os.system("python compute_mean_and_std_all.py")

    if create_pdfs:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        subdirectories = csv_tools.find_direct_subdirectories(base_dir)
        for subdirectory in subdirectories:
                case = subdirectory.split(os.sep)[-1] # e.g. 1_single_fracture

                if case[0] in ["1"]:#["1", "2", "3", "4"]:
                    # Run the file case/run_all.py
                    run_all = os.path.join(subdirectory, "run_all.py")
                    print(f"Running {run_all}")
                    os.system(f"python {run_all}")

                    plots_directory = os.path.join('plots', subdirectory).replace("scripts", "plots")
                    os.system(f"python combine_pdfs.py {plots_directory}")

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