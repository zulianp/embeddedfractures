import os

import fracture_plotter.utils.plot_routines as plot
from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines import *


def create_places_and_methods_dict(
    refinement_indices=None, places_and_methods=None, paths=None
):  # refinement indices included just to match function signature in toher files
    places_and_methods_dict = {k: places_and_methods.copy() for k in refinement_indices}

    for cond in [0, 1, 2]:
        for place, methods in places_and_methods.items():
            for method in methods:
                folder = os.path.join(paths.results_dir, place, method).replace(
                    r"\_", "_"
                )
                file_path = os.path.join(folder, f"dot_cond_{cond}.csv").replace(
                    r"\_", "_"
                )
                if not os.path.exists(file_path):
                    del places_and_methods_dict[cond][place]
                    break
    return places_and_methods_dict


def plot_cond_over_time(
    places_and_methods,
    cond,
    ax,
    title,
    region,
    region_pos,
    ylim,
    show_legend=False,
    fontsize=30,
):
    paths = get_paths(__file__)

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method)
            data_file = os.path.join(folder, f"dot_cond_{cond}.csv").replace("\\_", "_")

            # TODO: Remove this, this is just here for testing purposes
            if cond > 0 and place == "mean":
                data_file = os.path.join(folder, f"dot_cond_0.csv").replace("\\_", "_")

            label = place if place == "mean" else f"{place}-{method}"

            plot.plot_over_time(
                case=paths.case,
                filename=data_file,
                label=label,
                title=title,
                region=region,
                region_pos=region_pos,
                ax=ax,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                fontsize=fontsize,
                show_legend=show_legend,
                ylim=ylim,
            )


def run_pot(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=25,
    refinement_indices=None,
    titles=None,
):
    paths = get_paths(__file__)
    if refinement_indices is None:
        refinement_indices = [0, 1, 2]
    if titles is None:
        titles = [f"Refinement {ref}" for ref in refinement_indices]
    conds = [0, 1, 2]  # List of conditions
    regions = [1, 10, 11]  # Single region for this case # regions: 1, 10, 11

    # Setup figures and axes for each condition and region
    for cond, title in zip(conds, titles):
        fig, axes_list = plot.setup_figure(
            id_offset=cond, num_axes=len(regions), ylim=(0, 0.4 if cond else 0.475)
        )

        for region_pos, region in enumerate(regions):
            ax = axes_list[region_pos]
            show_legend = region_pos == 1  # Ensure the legend is shown in this case

            # TODO: this is the original which should be brought back
            # places_and_methods_arg = plot.get_places_and_methods_arg(
            #     places_and_methods=places_and_methods, ref=cond
            # )
            # For TESTING purposes, as requested, we use the same places_and_methods for all refinements
            places_and_methods_arg = plot.get_places_and_methods_arg(
                places_and_methods=places_and_methods, ref=0
            )

            plot_cond_over_time(
                places_and_methods=places_and_methods_arg,
                cond=cond,
                ax=ax,
                title=title,
                region=region,
                region_pos=region_pos,
                ylim=(0, 0.4 if cond else 0.475),
                show_legend=show_legend,
                fontsize=fontsize,
            )

            # Add the legend directly to the figure (on the first region)
            if region_pos == 1:  # or region_pos == 1 for middle
                plot.plot_legend_in_middle(ax=ax, fontsize=fontsize)

        # Save figure without creating a separate legend file
        plot.save(
            ID=cond,
            filename=f"pot_cond_{cond}",
            plots_dir=paths.plots_dir,
            fontsize=subfig_fontsize,
            starting_from=3 * cond,
        )


if __name__ == "__main__":
    run_pot()
