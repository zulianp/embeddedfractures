# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os

curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
case = curr_dir.split(os.sep)[-1] # case we are dealing with
files = [f"{curr_dir}/{case}_pol_p_line_0", 
         f"{curr_dir}/{case}_pot_fracture_3"
         ]

# Change working directory to the one containing this file 
os.chdir(curr_dir)
for f in files:
    os.system(f"pdflatex {f}.tex")
    f_pdf = f"{f}.pdf"
    os.system(f"pdfcrop {f_pdf}")
    os.system(f"mv {f_pdf} {f}-crop.pdf")
    os.system(f"mv {f}-crop.pdf ../../plots/{case}/")
    
    # Check if {f}.aux exists and remove it
    if os.path.exists(f"{f}.aux"):
        os.system(f"rm {f}.aux")
    # Check if {f}.log exists and remove it
    if os.path.exists(f"{f}.log"):
        os.system(f"rm {f}.log")




