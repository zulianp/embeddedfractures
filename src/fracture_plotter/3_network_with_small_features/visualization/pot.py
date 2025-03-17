import os

import plotroutines as plot

from fracture_plotter.utils.general import get_paths


def plot_data_over_time(places_and_methods, ref, ax, ID, title, fontsize=30):
    paths = get_paths(__file__)
    for place, methods in places_and_methods.items():
        for method in methods:
            folder = os.path.join(paths.results_dir, place, method).replace(r"\_", "_")
            data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace(r"\_", "_")
            label = place if place == "mean" else f"{place}-{method}"
            plot.plot_over_time(
                filename=data,
                label=label,
                ref=ref,
                ID=ID,
                title=title,
                ax=ax,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                fontsize=fontsize,
                show_legend=False,
            )


def run_pot(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=25,
):
    paths = get_paths(__file__)
    titles = ["$\\sim 30k$ cells", "$\\sim 150k$ cells"]
    refinement_index = [0, 1]
    for ID in range(8):
        fig, axes = plot.setup_figure(
            id_offset=ID, num_axes=len(refinement_index), ylim=(-0.01, 1.01)
        )
        for title, ref, ax in zip(titles, refinement_index, axes):
            plot_data_over_time(
                places_and_methods=places_and_methods,
                ref=ref,
                ax=ax,
                ID=ID,
                title=title,
                fontsize=fontsize,
            )
        plot.plot_legend_in_middle(fig=fig, ax1=axes[0], ax2=axes[1], fontsize=fontsize)
    plot.save_over_time(
        filename=f"{paths.case}_pot",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )


if __name__ == "__main__":
    run_pot()
