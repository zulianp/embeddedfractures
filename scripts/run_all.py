import os 
import utils.csv as csv_tools

# In case you want to exclude other cases, for instance, when debugging
compute_mean_and_std_all = True
create_pdfs = True
copy_pdfs_to_overleaf = True

if compute_mean_and_std_all:
    # Compute mean and standard deviation for all cases
    os.system("python scripts/compute_mean_and_std_all.py")

if create_pdfs:")
    # Get the directory in which this file resides
    base_dir = os.path.dirname(os.path.realpath(__file__))
    # Get all direct subdirectories of the base directory
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)
    # Iterate over all subdirectories
    for subdirectory in subdirectories:
            # Split based on os.path separator and get the last element
            case = subdirectory.split(os.sep)[-1]

            if case[0] in ["1", "2", "3", "4"]: 
                # Run the file case/run_all.py
                run_all = os.path.join(subdirectory, "run_all.py")
                print(f"Running {run_all}")
                os.system(f"python {run_all}")

if copy_pdfs_to_overleaf:
    # Copy all PDF files to overleaf_embedded_fractures/figures/pdf/
    base_dir = "plots"
    subdirectories = csv_tools.find_direct_subdirectories(base_dir)
    for subdirectory in subdirectories:
        # List the files in subdirectory
        files = os.listdir(subdirectory)
        
        # Copy all files to ../overleaf_embedded_fractures/figures/pdf/
        for file in files:
            if file.endswith(".pdf"):
                src = os.path.join(subdirectory, file)
                dst = os.path.join("../overleaf_embedded_fractures/figures/pdf", file)
                os.system(f"cp {src} {dst}")
