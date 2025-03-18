import os

import fracture_plotter.utils.plot_routines as plot
from fracture_plotter.utils.general import get_paths


def plot_data_over_lines(
    places_and_methods, ax, title, line_idx, ylim, xlim, fontsize=30
):
    paths = get_paths(__file__)

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dol_line_{line_idx}.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")
            plot.plot_over_line(
                case=paths.case_num,
                filename=data,
                label=label,
                ID=plot.id_p_0_matrix + line_idx,
                title=title,
                ax=ax,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                fontsize=fontsize,
                show_legend=False,
            )

    # Set axis limits
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)


def run_pol(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=25,
):
    paths = get_paths(__file__)

    fig_p_0, ax_p_0 = plot.plt.figure(plot.id_p_0_matrix + 11), plot.plt.subplot(
        ylim=(-50, 720), xlim=(-100, 1800)
    )
    fig_p_1, ax_p_1 = plot.plt.figure(plot.id_p_1_matrix + 11), plot.plt.subplot(
        ylim=(-20, 280), xlim=(-100, 1800)
    )

    plot_data_over_lines(
        places_and_methods=places_and_methods,
        ax=ax_p_0,
        title="Line 0",
        line_idx=0,
        xlim=(-100, 1800),
        ylim=(-50, 720),
        fontsize=fontsize,
    )

    plot_data_over_lines(
        places_and_methods=places_and_methods,
        ax=ax_p_1,
        title="Line 1",
        line_idx=1,
        xlim=(-100, 1800),
        ylim=(-20, 280),
        fontsize=fontsize,
    )

    # Add legend in one of the plots (middle or specific plot)
    plot.plot_legend_in_middle(ax=ax_p_0, fontsize=fontsize)
    plot.plot_legend_in_middle(ax=ax_p_1, fontsize=fontsize)

    # Save figures
    plot.save(
        ID=plot.id_p_0_matrix,
        filename=f"{paths.case}_pol_line_0",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )
    plot.save(
        ID=plot.id_p_1_matrix,
        filename=f"{paths.case}_pol_line_1",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )


if __name__ == "__main__":
    run_pol()
