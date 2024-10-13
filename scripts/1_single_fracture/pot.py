import os
import numpy as np
import plotroutines as plot

def plot_data_over_time(places_and_methods, results_dir, ref, axes_intc_matrix, axes_intc_fracture, axes_outflux, title, show_legend=False):
    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method)
            data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace("\_", "_")

            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

            plot.plot_over_time(data, label, ref, plot.id_intc_matrix, title, axes_intc_matrix,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=show_legend, ylim=(0-10, 175+10))
            plot.plot_over_time(data, label, ref, plot.id_intc_fracture, title, axes_intc_fracture,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=show_legend, ylim=(0, 0.45))
            plot.plot_over_time(data, label, ref, plot.id_outflux, title, axes_outflux,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=show_legend, ylim=(0-0.00000005, 0.0000014+0.00000005))

def run_pot():
    curr_dir, plots_dir, results_dir, utils_dir = plot.get_paths()
    case = curr_dir.split(os.sep)[-1]  # case we are dealing with
    titles = np.array(['$\\sim 1k$ cells', '$\\sim 10k$ cells', '$\\sim 100k$ cells'])
    refinement_index = [0, 1, 2]
    places_and_methods = {"USI": ["FEM\_LM"], "mean": ["key"]}

    # Setup figures and axes
    fig_intc_matrix, axes_intc_matrix_list = plot.setup_figure(plot.id_intc_matrix, 3, ylim=(0-10, 175+10))
    fig_intc_fracture, axes_intc_fracture_list = plot.setup_figure(plot.id_intc_fracture, 3, ylim=(0, 0.45))
    fig_outflux, axes_outflux_list = plot.setup_figure(plot.id_outflux, 3, ylim=(0-0.00000005, 0.0000014+0.00000005))

    # Plot data
    for title, ref, idx, axes_intc_matrix, axes_intc_fracture, axes_outflux in zip(titles, refinement_index, range(3), axes_intc_matrix_list, axes_intc_fracture_list, axes_outflux_list):
        show_legend = (idx == 1)  # Show the legend only for the middle subplot (index 1, subfigure b)
        plot_data_over_time(places_and_methods, results_dir, ref, axes_intc_matrix, axes_intc_fracture, axes_outflux, title, show_legend)

        # Only add the legend to the middle subplot (subfigure b)
        if idx == 1:
            plot.plot_legend_in_middle(axes_intc_matrix)
            plot.plot_legend_in_middle(axes_intc_fracture)
            plot.plot_legend_in_middle(axes_outflux)

    # Save figures with integrated legends
    plot.save(plot.id_intc_matrix, f"{case}_pot_c_matrix")
    plot.save(plot.id_intc_fracture, f"{case}_pot_c_fracture")
    plot.save(plot.id_outflux, f"{case}_pot_outflux")


if __name__ == "__main__":
    run_pot()
