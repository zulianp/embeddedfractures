# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import plotroutines as plot

def run_pol():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    results_dir = curr_dir.replace('scripts', 'results')
    case = curr_dir.split(os.sep)[-1] # case we are dealing with

    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    fig_p_0 = plot.plt.figure(plot.id_p_0_matrix+11)
    fig_p_1 = plot.plt.figure(plot.id_p_1_matrix+11)
    ax_p_0 = fig_p_0.add_subplot(ylim=(-50, 720), xlim=(-100, 1800))
    ax_p_1 = fig_p_1.add_subplot(ylim=(-20, 280), xlim=(-100, 1800))

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method)
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

            title = "line 2"
            data = os.path.join(folder, "dol_line_0.csv").replace("\_", "_")
            if place.replace("\_", "_") != "mean":
                    plot.plot_over_line(data, label,
                            plot.id_p_0_matrix, title, ax_p_0,
                            plot.linestyle[place][method], plot.color[place][method],
                            has_legend=False)
            else:
                    std_data = data.replace("mean", "std")
                    plot.plot_mean_and_std_over_line(data, std_data, label,
                            plot.id_p_0_matrix, title, ax_p_0,
                            plot.linestyle[place][method], plot.color[place][method],
                            has_legend=False)

            title = "line 1"
            data = os.path.join(folder, "dol_line_1.csv").replace("\_", "_")
            if place.replace("\_", "_") != "mean":
                    plot.plot_over_line(data, label,
                                    plot.id_p_1_matrix, title, ax_p_1,
                                    plot.linestyle[place][method], plot.color[place][method],
                                    has_legend=False)
            else:
                    std_data = data.replace("mean", "std")
                    plot.plot_mean_and_std_over_line(data, std_data, label,
                                    plot.id_p_1_matrix, title, ax_p_1,
                                    plot.linestyle[place][method], plot.color[place][method],
                                    has_legend=False)

    # save figures
    ax_title = "\\textbf{subfig. b}"
    plot.save(plot.id_p_0_matrix, f"{case}_pol_line_2", ax_title=ax_title)
    ax_title = "\\textbf{subfig. a}"
    plot.save(plot.id_p_1_matrix, f"{case}_pol_line_1", ax_title=ax_title)

    ncol = 4
    for place in places_and_methods:
        for method in places_and_methods[place]:
            label = "\\texttt{" + place + ("-" + method if place.replace("\_", "_") != "mean" else "") + "}"
            plot.plot_legend(label, plot.id_p_0_matrix_legend, plot.linestyle[place][method],
                             plot.color[place][method], ncol)

            plot.plot_legend(label, plot.id_p_1_matrix_legend, plot.linestyle[place][method],
                                 plot.color[place][method], ncol)

    plot.save(plot.id_p_0_matrix_legend, f"{case}_pol_p_0_matrix_legend")
    plot.crop_pdf(f"{case}_pol_p_0_matrix_legend")
    plot.save(plot.id_p_1_matrix_legend, f"{case}_pol_p_1_matrix_legend")
    plot.crop_pdf(f"{case}_pol_p_1_matrix_legend")


if __name__ == "__main__":
    run_pol()