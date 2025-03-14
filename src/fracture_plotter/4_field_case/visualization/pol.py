import os

import plotroutines as plot

from fracture_plotter.utils.general import get_paths


def plot_data_over_lines(places_and_methods, ax, title, line_idx, ylim, xlim):
    paths = get_paths(__file__)

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dol_line_{line_idx}.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")
            plot.plot_over_line(
                data,
                label,
                plot.id_p_0_matrix + line_idx,
                title,
                ax,
                plot.linestyle[place][method],
                plot.color[place][method],
                has_legend=False,
                
            )

    # Set axis limits
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)


def run_pol(places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]}):
    paths = get_paths(__file__)

    fig_p_0, ax_p_0 = plot.plt.figure(plot.id_p_0_matrix + 11), plot.plt.subplot(
        ylim=(-50, 720), xlim=(-100, 1800)
    )
    fig_p_1, ax_p_1 = plot.plt.figure(plot.id_p_1_matrix + 11), plot.plt.subplot(
        ylim=(-20, 280), xlim=(-100, 1800)
    )

    # Plot data for line 0 and line 1
    plot_data_over_lines(
        places_and_methods, ax_p_0, "Line 2", 0, (-50, 720), (-100, 1800)
    )
    plot_data_over_lines(
        places_and_methods, ax_p_1, "Line 1", 1, (-20, 280), (-100, 1800)
    )

    # Add legend in one of the plots (middle or specific plot)
    plot.plot_legend_in_middle(ax_p_0)
    plot.plot_legend_in_middle(ax_p_1)

    # Save figures
    plot.save(
        plot.id_p_0_matrix,
        f"{paths.case}_pol_line_2",
        ax_title="\\textbf{subfig. b}",
        plots_dir=paths.plots_dir,
    )
    plot.save(
        plot.id_p_1_matrix,
        f"{paths.case}_pol_line_1",
        ax_title="\\textbf{subfig. a}",
        plots_dir=paths.plots_dir,
    )


if __name__ == "__main__":
    run_pol()
