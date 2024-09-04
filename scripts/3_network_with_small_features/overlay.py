# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os

curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
case = curr_dir.split(os.sep)[-1] # case we are dealing with
files = [f"{curr_dir}/{case}_pol_p_line_0", f"{curr_dir}/{case}_pot_fracture_3"]

for f in files:
    os.system("pdflatex " + f)
    f_pdf = f + ".pdf"
    os.system("pdfcrop " + f_pdf)
    os.system("mv " + f + f"-crop.pdf plots/{case}/{case}" + f_pdf )


