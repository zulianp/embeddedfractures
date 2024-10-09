# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import plotroutines as plot

def run_percentiles():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    case = curr_dir.split(os.sep)[-1] # case we are dealing with

    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    fig_p_matrix = plot.plt.figure(plot.id_p_matrix+11, figsize=(16, 6))
    fig_p_matrix.subplots_adjust(hspace=0, wspace=0)
    fig_c_matrix = plot.plt.figure(plot.id_c_matrix+11, figsize=(16, 6))
    fig_c_matrix.subplots_adjust(hspace=0, wspace=0)
    fig_c_fracture = plot.plt.figure(plot.id_c_fracture+11, figsize=(16, 6))
    fig_c_fracture.subplots_adjust(hspace=0, wspace=0)

    for ref in ["0", "1", "2"]:
        axes_p_matrix = fig_p_matrix.add_subplot(1, 3, int(ref) + 1, ylim=(1-0.1, 4+0.1))
        axes_c_matrix = fig_c_matrix.add_subplot(1, 3, int(ref) + 1, ylim=(0-0.0005, 0.01+0.0005))
        axes_c_fracture = fig_c_fracture.add_subplot(1, 3, int(ref) + 1, ylim=(0.0075, 0.0101))
        plot.plot_percentiles(ref, plot.id_p_matrix, places_and_methods, axes_p_matrix)
        plot.plot_percentiles(ref, plot.id_c_matrix, places_and_methods, axes_c_matrix)
        plot.plot_percentiles(ref, plot.id_c_fracture, places_and_methods, axes_c_fracture)

    # save figures
    plot.save(plot.id_p_matrix, f"{case}_pol_p_matrix_percentile_90_10", starting_from=3)
    plot.save(plot.id_c_matrix, f"{case}_pol_c_matrix_percentile_90_10", starting_from=3)
    plot.save(plot.id_c_fracture, f"{case}_pol_c_fracture_percentile_90_10", starting_from=3)
