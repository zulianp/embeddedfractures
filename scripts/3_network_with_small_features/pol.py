# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import plotroutines as plot
from matplotlib import rc

def run_pol():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    results_dir = curr_dir.replace('scripts', 'results')
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    titles = ["$\\sim 30k$ cells", "$\\sim 150k$ cells"]
    refinement_index = ["0", "1"]

    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    fig_p_0 = plot.plt.figure(plot.id_p_0_matrix+11, figsize=(16, 6))
    fig_p_0.subplots_adjust(hspace=0, wspace=0)
    fig_p_1 = plot.plt.figure(plot.id_p_1_matrix+11, figsize=(16, 6))
    fig_p_1.subplots_adjust(hspace=0, wspace=0)

    for title, ref in zip(titles, refinement_index):

        ax_p_0 = fig_p_0.add_subplot(1, 2, int(ref) + 1, ylim=(0.03-0.005, 0.07+0.01))
        ax_p_1 = fig_p_1.add_subplot(1, 2, int(ref) + 1, ylim=(0.02-0.001, 0.07+0.005))

        for place in places_and_methods:
            for method in places_and_methods[place]:
                folder = os.path.join(results_dir, place, method)
                label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

                data = os.path.join(folder, f"dol_line_0_refinement_{ref}.csv").replace("\_", "_")
                if place.replace("\_", "_") != "mean":
                    plot.plot_over_line(data, label, ref,
                                        plot.id_p_0_matrix, title, ax_p_0,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, fmt="%1.2f")
                else:
                    std_data = data.replace("mean", "std")
                    plot.plot_mean_and_std_over_line(data, std_data, label, ref,
                                                     plot.id_p_0_matrix, title, ax_p_0,
                                                     plot.linestyle[place][method], plot.color[place][method],
                                                     has_legend=False, fmt="%1.2f")

                data = os.path.join(folder, f"dol_line_1_refinement_{ref}.csv").replace("\_", "_")
                if place.replace("\_", "_") != "mean":
                    plot.plot_over_line(data, label, ref,
                                        plot.id_p_1_matrix, title, ax_p_1,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, fmt="%1.2f")
                else:
                    std_data = data.replace("mean", "std")
                    plot.plot_mean_and_std_over_line(data, std_data, label, ref,
                                                     plot.id_p_1_matrix, title, ax_p_1,
                                                     plot.linestyle[place][method], plot.color[place][method],
                                                     has_legend=False, fmt="%1.2f")

        # Reference
        folder = os.path.join(results_dir, 'USTUTT', 'MPFA')
        ref_label = "USTUTT\_MPFA\_refined"
        data = os.path.join(folder, "dol_line_0_refinement_5.csv")
        plot.plot_over_line(data, ref_label, ref,
                            plot.id_p_0_matrix, title, ax_p_0,
                            plot.linestyle["USTUTT"]["reference"], plot.color["USTUTT"]["reference"],
                            has_legend=False, fmt="%1.2f")
        data = os.path.join(folder, "dol_line_1_refinement_5.csv")
        plot.plot_over_line(data, ref_label, ref,
                            plot.id_p_1_matrix, title, ax_p_1,
                            plot.linestyle["USTUTT"]["reference"], plot.color["USTUTT"]["reference"],
                            has_legend=False, fmt="%1.2f")

    # save figures
    plot.save(plot.id_p_0_matrix, f"{case}_pol_p_line_0")
    plot.save(plot.id_p_1_matrix, f"{case}_pol_p_line_1")

    ncol = 4
    for place in places_and_methods:
        for method in places_and_methods[place]:
            label = "\\texttt{" + place + ("-" + method if place.replace("\_", "_") != "mean" else "") + "}"
            plot.plot_legend(label, plot.id_p_0_matrix_legend, plot.linestyle[place][method],
                             plot.color[place][method], ncol)

            plot.plot_legend(label, plot.id_p_1_matrix_legend, plot.linestyle[place][method],
                                 plot.color[place][method], ncol)

    # add reference to legend
    plot.plot_legend("reference", plot.id_p_0_matrix_legend, plot.linestyle["USTUTT"]["reference"],
                     plot.color["USTUTT"]["reference"], ncol)

    plot.plot_legend("reference", plot.id_p_1_matrix_legend, plot.linestyle["USTUTT"]["reference"],
                     plot.color["USTUTT"]["reference"], ncol)

    plot.save(plot.id_p_0_matrix_legend, f"{case}_pol_p_0_matrix_legend")
    plot.crop_pdf(f"{case}_pol_p_0_matrix_legend")
    plot.save(plot.id_p_1_matrix_legend, f"{case}_pol_p_1_matrix_legend")
    plot.crop_pdf(f"{case}_pol_p_1_matrix_legend")


if __name__ == "__main__":
    run_pol()