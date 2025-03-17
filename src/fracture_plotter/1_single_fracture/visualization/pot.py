import os

import numpy as np
import plotroutines as plot

from fracture_plotter.utils.general import get_paths


def plot_data_over_time(
    places_and_methods,
    ref,
    axes_intc_matrix,
    axes_intc_fracture,
    axes_outflux,
    title,
    show_legend=False,
    fontsize=30,
):
    paths = get_paths(__file__)

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method)
            data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

            plot.plot_over_time(
                filename=data,
                label=label,
                ref=ref,
                ID=plot.id_intc_matrix,
                title=title,
                ax=axes_intc_matrix,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                fontsize=fontsize,
                show_legend=show_legend,
                ylim=(0 - 10, 175 + 10),
            )
            plot.plot_over_time(
                filename=data,
                label=label,
                ref=ref,
                ID=plot.id_intc_fracture,
                title=title,
                ax=axes_intc_fracture,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                fontsize=fontsize,
                show_legend=show_legend,
                ylim=(0, 0.45),
            )
            plot.plot_over_time(
                filename=data,
                label=label,
                ref=ref,
                ID=plot.id_outflux,
                title=title,
                ax=axes_outflux,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                fontsize=fontsize,
                show_legend=show_legend,
                ylim=(0 - 0.00000005, 0.0000014 + 0.00000005),
            )


def run_pot(places_and_methods={"mean": ["key"]}, fontsize=30, subfig_fontsize=12):
    paths = get_paths(__file__)

    titles = np.array(["$\\sim 1k$ cells", "$\\sim 10k$ cells", "$\\sim 100k$ cells"])
    refinement_index = [0, 1, 2]

    # Setup figures and axes
    fig_intc_matrix, axes_intc_matrix_list = plot.setup_figure(
        plot.id_intc_matrix, 3, ylim=(0 - 10, 175 + 10)
    )
    fig_intc_fracture, axes_intc_fracture_list = plot.setup_figure(
        plot.id_intc_fracture, 3, ylim=(0, 0.45)
    )
    fig_outflux, axes_outflux_list = plot.setup_figure(
        plot.id_outflux, 3, ylim=(0 - 0.00000005, 0.0000014 + 0.00000005)
    )

    # Plot data
    for title, ref, idx, axes_intc_matrix, axes_intc_fracture, axes_outflux in zip(
        titles,
        refinement_index,
        range(3),
        axes_intc_matrix_list,
        axes_intc_fracture_list,
        axes_outflux_list,
    ):
        show_legend = (
            idx == 1
        )  # Show the legend only for the middle subplot (index 1, subfigure b)
        plot_data_over_time(
            places_and_methods=places_and_methods,
            ref=ref,
            axes_intc_matrix=axes_intc_matrix,
            axes_intc_fracture=axes_intc_fracture,
            axes_outflux=axes_outflux,
            title=title,
            show_legend=show_legend,
            fontsize=fontsize,
        )

        # Only add the legend to the middle subplot (subfigure b)
        if idx == 1:
            plot.plot_legend_in_middle(axes_intc_matrix)
            plot.plot_legend_in_middle(axes_intc_fracture)
            plot.plot_legend_in_middle(axes_outflux)

    # Save figures with integrated legends
    plot.save(
        ID=plot.id_intc_matrix,
        filename=f"{paths.case}_pot_c_matrix",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )
    plot.save(
        ID=plot.id_intc_fracture,
        filename=f"{paths.case}_pot_c_fracture",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )
    plot.save(
        ID=plot.id_outflux,
        filename=f"{paths.case}_pot_outflux",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )


if __name__ == "__main__":
    run_pot()
