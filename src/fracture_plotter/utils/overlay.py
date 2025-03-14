# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os


def run_overlay(files, paths):
    # Change working directory to the one containing this file
    os.chdir(paths.tex_dir)
    for f in files:
        cmd = (
            f'pdflatex "\\def\\plotsPath{{{paths.plots_dir + os.sep}}}'
            f'\\def\\figuresPath{{{paths.tex_figs_dir + os.sep}}}\\input{{{f}.tex}}"'
        )
        os.system(cmd)
        f_pdf = f"{f}.pdf"
        os.system(f"pdfcrop {f_pdf} {f}-overlay.pdf")
        os.system(f"mv {f}-overlay.pdf {os.path.join(paths.plots_dir, paths.case)}.pdf")
        os.system(f"rm {f_pdf}")
        os.system(
            f"rm {os.path.join(paths.plots_dir, paths.case, f_pdf.split(os.path.sep)[-1])}"
        )

        os.system(f"rm *.aux")
        os.system(f"rm *.log")
