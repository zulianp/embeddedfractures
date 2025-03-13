# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os


def run_overlay(files, paths):
    # Change working directory to the one containing this file
    os.chdir(paths.tex_dir)
    for f in files:
        cmd = (
            f'pdflatex "\\def\\plotsPath{{{paths.plots_dir}/}}'
            f'\\def\\figuresPath{{{paths.tex_figs_dir}}}\\input{{{f}.tex}}"'
        )
        os.system(cmd)
        f_pdf = f"{f}.pdf"
        os.system(f"pdfcrop {f_pdf} {f}-overlay.pdf")
        os.system(f"mv {f}-overlay.pdf {paths.plots_dir}/{paths.case}/")
        os.system(f"rm {f_pdf}")
        os.system(f"rm {paths.plots_dir}/{paths.case}/{f_pdf.split(os.path.sep)[-1]}")

        # Check if {f}.aux exists and remove it
        # if os.path.exists(f"{f}.aux"):
        #     os.system(f"rm {f}.aux")

        # Check if {f}.log exists and remove it
        # if os.path.exists(f"{f}.log"):
        #     os.system(f"rm {f}.log")
