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
    for place, methods in places_and_methods.items():
        for method in methods:
            folder = os.path.join(paths.results_dir, place, method)
            data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace("\_", "_")
            label = place if place == "mean" else f"{place}-{method}"
            common = {
                "filename": data,
                "label": label,
                "ref": ref,
                "title": title,
                "linestyle": plot.linestyle[place][method],
                "color": plot.color[place][method],
                "fontsize": fontsize,
                "show_legend": show_legend,
            }
            plot.plot_over_time(
                ID=plot.id_intc_matrix, ax=axes_intc_matrix, ylim=(-10, 185), **common
            )
            plot.plot_over_time(
                ID=plot.id_intc_fracture,
                ax=axes_intc_fracture,
                ylim=(0, 0.45),
                **common,
            )
            plot.plot_over_time(
                ID=plot.id_outflux,
                ax=axes_outflux,
                ylim=(-0.00000005, 0.00000145),
                **common,
            )


def run_pot(places_and_methods={"mean": ["key"]}, fontsize=30, subfig_fontsize=12):
    paths = get_paths(__file__)
    titles = np.array(["$\\sim 1k$ cells", "$\\sim 10k$ cells", "$\\sim 100k$ cells"])
    refinement_index = [0, 1, 2]

    fig_intc_matrix, axes_intc_matrix_list = plot.setup_figure(
        id_offset=plot.id_intc_matrix, num_axes=len(refinement_index), ylim=(-10, 185)
    )
    fig_intc_fracture, axes_intc_fracture_list = plot.setup_figure(
        id_offset=plot.id_intc_fracture, num_axes=len(refinement_index), ylim=(0, 0.45)
    )
    fig_outflux, axes_outflux_list = plot.setup_figure(
        id_offset=plot.id_outflux,
        num_axes=len(refinement_index),
        ylim=(-0.00000005, 0.00000145),
    )

    for idx, (title, ref, ax_matrix, ax_fracture, ax_outflux) in enumerate(
        zip(
            titles,
            refinement_index,
            axes_intc_matrix_list,
            axes_intc_fracture_list,
            axes_outflux_list,
        )
    ):
        show_legend = idx == 1
        plot_data_over_time(
            places_and_methods=places_and_methods,
            ref=ref,
            axes_intc_matrix=ax_matrix,
            axes_intc_fracture=ax_fracture,
            axes_outflux=ax_outflux,
            title=title,
            show_legend=show_legend,
            fontsize=fontsize,
        )
        if show_legend:
            for ax in (ax_matrix, ax_fracture, ax_outflux):
                plot.plot_legend_in_middle(ax=ax, fontsize=fontsize)

    for ID, suffix in (
        (plot.id_intc_matrix, "pot_c_matrix"),
        (plot.id_intc_fracture, "pot_c_fracture"),
        (plot.id_outflux, "pot_outflux"),
    ):
        plot.save(
            ID=ID,
            filename=f"{paths.case}_{suffix}",
            plots_dir=paths.plots_dir,
            fontsize=subfig_fontsize,
        )


if __name__ == "__main__":
    run_pot()
