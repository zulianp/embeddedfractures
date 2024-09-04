# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os

curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
case = curr_dir.split(os.sep)[-1] # case we are dealing with
files = [f"{curr_dir}/{case}_pol_c_fracture", f"{curr_dir}/{case}_pol_c_matrix",
         f"{curr_dir}/{case}_pol_p_matrix", f"{curr_dir}/{case}_pot_outflux"]

for f in files:
    os.system("pdflatex " + os.path.join(curr_dir, f))
    f_pdf = f + ".pdf"
    os.system("pdfcrop " + f_pdf)
    os.system("mv " + f + f"-crop.pdf plots/{case}/{case}" + f_pdf )


