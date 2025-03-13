# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import numpy as np
import plotroutines as plot

def run_percentiles(places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]}):
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    case = curr_dir.split(os.sep)[-1] # case we are dealing with

    for ref in ["0", "1"]:
        fig = plot.plt.figure(int(ref)+11)
        fig.subplots_adjust(hspace=0, wspace=0)

        if ref == "0":
            ax = fig.add_subplot(ylim=(-50, 720), xlim=(-100, 1800))
        else:
            ax = fig.add_subplot(ylim=(-20, 280), xlim=(-100, 1800))
        plot.plot_percentiles(ref, places_and_methods, ax)

        # save figures
        if ref == "0":
            ax_title = "\\textbf{subfig. d}"
        else:
            ax_title = "\\textbf{subfig. c}"

        plot.save(int(ref), f"{case}_pol_p_line_"+ref+"_matrix_percentile_90_10", ax_title=ax_title)

if __name__ == "__main__":
    run_percentiles()