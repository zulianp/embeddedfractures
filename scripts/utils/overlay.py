# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os

def run_overlay(files, working_directory):
    # Change working directory to the one containing this file
    os.chdir(working_directory)
    case = working_directory.split("/")[-1]
    for f in files:
        os.system(f"pdflatex {f}.tex")
        f_pdf = f"{f}.pdf"
        os.system(f"pdfcrop {f_pdf} {f}-overlay.pdf")
        os.system(f"mv {f}-overlay.pdf ../../plots/{case}/")
        os.system(f"rm {f}.pdf")

        # Check if {f}.aux exists and remove it
        if os.path.exists(f"{f}.aux"):
            os.system(f"rm {f}.aux")

        # Check if {f}.log exists and remove it
        if os.path.exists(f"{f}.log"):
            os.system(f"rm {f}.log")

