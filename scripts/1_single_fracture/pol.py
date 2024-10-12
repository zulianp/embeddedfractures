import os
import plotroutines as plot

def plot_data_over_lines(places_and_methods, results_dir, ref, axes_p_matrix, axes_c_matrix, axes_c_fracture, title, show_legend=False):
    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dol_refinement_{ref}.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

            # Pass show_legend flag to the plot function
            plot.plot_over_line(data, label, ref, plot.id_p_matrix, title, axes_p_matrix,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=show_legend)

            if place != "DTU":  # Only pressure for DTU
                plot.plot_over_line(data, label, ref, plot.id_c_matrix, title, axes_c_matrix,
                                    plot.linestyle[place][method], plot.color[place][method],
                                    has_legend=show_legend)
                plot.plot_over_line(data, label, ref, plot.id_c_fracture, title, axes_c_fracture,
                                    plot.linestyle[place][method], plot.color[place][method],
                                    has_legend=show_legend)

def run_pol():
    curr_dir = os.path.dirname(os.path.realpath(__file__))  # current directory
    results_dir = curr_dir.replace("scripts", "results")
    case = curr_dir.split(os.sep)[-1]  # case we are dealing with
    titles = ['$\\sim 1k$ cells', '$\\sim 10k$ cells', '$\\sim 100k$ cells']
    refinement_index = [0, 1, 2]
    places_and_methods = {"USI": ["FEM\_LM"], "mean": ["key"]}

    # Setup figures and axes
    fig_p_matrix, axes_p_matrix_list = plot.setup_figure(plot.id_p_matrix, 3, ylim=(1-0.1, 4+0.1))
    fig_c_matrix, axes_c_matrix_list = plot.setup_figure(plot.id_c_matrix, 3, ylim=(0-0.0005, 0.01+0.0005))
    fig_c_fracture, axes_c_fracture_list = plot.setup_figure(plot.id_c_fracture, 3, ylim=(0.0075, 0.0101))

    # Plot data
    for title, ref, idx, axes_p_matrix, axes_c_matrix, axes_c_fracture in zip(titles, refinement_index, range(3), axes_p_matrix_list, axes_c_matrix_list, axes_c_fracture_list):
        show_legend = (idx == 1)  # Show the legend only for the middle subplot (index 1, subfigure b)
        plot_data_over_lines(places_and_methods, results_dir, ref, axes_p_matrix, axes_c_matrix, axes_c_fracture, title, show_legend)

        # Add reference for USTUTT-MPFA
        ref_data = os.path.join(results_dir, "USTUTT/MPFA/dol_refinement_5.csv".replace("\_", "_"))
        plot.plot_over_line(ref_data, "reference", ref, plot.id_p_matrix, title, axes_p_matrix,
                            plot.linestyle["USTUTT"]["reference"], plot.color["USTUTT"]["reference"],
                            has_legend=show_legend)

        # Only add the legend to the middle subplot (subfigure b)
        if idx == 1:
            plot.plot_legend_in_middle(axes_p_matrix)
            plot.plot_legend_in_middle(axes_c_matrix)
            plot.plot_legend_in_middle(axes_c_fracture)

    # Save figures with integrated legends
    plot.save(ID=plot.id_p_matrix, filename=f"{case}_pol_p_matrix")
    plot.save(ID=plot.id_c_matrix, filename=f"{case}_pol_c_matrix")
    plot.save(ID=plot.id_c_fracture, filename=f"{case}_pol_c_fracture")


if __name__ == "__main__":
    run_pol()
