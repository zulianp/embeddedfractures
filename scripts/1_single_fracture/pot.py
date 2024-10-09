# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import numpy as np
import plotroutines as plot

def run_pot():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    results_dir = curr_dir.replace("scripts", "results")
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    titles = np.array(['$\\sim 1k$ cells', '$\\sim 10k$ cells', '$\\sim 100k$ cells'])
    refinement_index = ['0', '1', '2']

    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    fig_intc_matrix = plot.plt.figure(plot.id_intc_matrix+11, figsize=(16, 6))
    fig_intc_matrix.subplots_adjust(hspace=0, wspace=0)
    fig_intc_fracture = plot.plt.figure(plot.id_intc_fracture+11, figsize=(16, 6))
    fig_intc_fracture.subplots_adjust(hspace=0, wspace=0)
    fig_outflux = plot.plt.figure(plot.id_outflux+11, figsize=(16, 6))
    fig_outflux.subplots_adjust(hspace=0, wspace=0)

    for title, ref in zip(titles, refinement_index):

        axes_intc_matrix = fig_intc_matrix.add_subplot(1, 3, int(ref) + 1, ylim=(0-10, 175+10))
        axes_intc_fracture = fig_intc_fracture.add_subplot(1, 3, int(ref) + 1, ylim=(0, 0.45))
        axes_outflux = fig_outflux.add_subplot(1, 3, int(ref) + 1, ylim=(0-0.00000005, 0.0000014+0.00000005))

        for place in places_and_methods:
            for method in places_and_methods[place]:
                folder = os.path.join(results_dir, place, method)
                data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace("\_", "_")

                label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

                if place.replace("\_", "_") != "mean":
                    plot.plot_over_time(data, label, ref, plot.id_intc_matrix, title, axes_intc_matrix,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, ylim=(0-10, 175+10))
                    plot.plot_over_time(data, label, ref, plot.id_intc_fracture, title, axes_intc_fracture,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, ylim=(0, 0.45))
                    plot.plot_over_time(data, label, ref, plot.id_outflux, title, axes_outflux,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, ylim=(0-0.00000005, 0.0000014+0.00000005))
                else:
                    std_data = data.replace("mean", "std")

                    plot.plot_mean_and_std_over_time(data, std_data, label, ref, plot.id_intc_matrix, title, axes_intc_matrix,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, ylim=(0-10, 175+10))
                    plot.plot_mean_and_std_over_time(data, std_data, label, ref, plot.id_intc_fracture, title, axes_intc_fracture,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, ylim=(0, 0.45))
                    plot.plot_mean_and_std_over_time(data, std_data, label, ref, plot.id_outflux, title, axes_outflux,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, ylim=(0-0.00000005, 0.0000014+0.00000005))

    # save figures
    plot.save(plot.id_intc_matrix, f"{case}_pot_c_matrix")
    plot.save(plot.id_intc_fracture, f"{case}_pot_c_fracture")
    plot.save(plot.id_outflux, f"{case}_pot_outflux")

    # Plot legend
    ncol = 4
    for place in places_and_methods:
        for method in places_and_methods[place]:
            label = "\\texttt{" + place + ("-" + method if place.replace("\_", "_") != "mean" else "") + "}"
            plot.plot_legend(label, plot.id_intc_matrix_legend, plot.linestyle[place][method],
                             plot.color[place][method], ncol)
            plot.plot_legend(label, plot.id_intc_fracture_legend, plot.linestyle[place][method],
                             plot.color[place][method], ncol)
            plot.plot_legend(label, plot.id_outflux_legend, plot.linestyle[place][method],
                             plot.color[place][method], ncol)

    plot.save(plot.id_intc_matrix_legend, f"{case}_pot_c_matrix_legend")
    plot.crop_pdf(f"{case}_pot_c_matrix_legend")
    plot.save(plot.id_intc_fracture_legend, f"{case}_pot_c_fracture_legend")
    plot.crop_pdf(f"{case}_pot_c_fracture_legend")
    plot.save(plot.id_outflux_legend, f"{case}_pot_outflux_legend")
    plot.crop_pdf(f"{case}_pot_outflux_legend")
