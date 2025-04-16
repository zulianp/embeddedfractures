import os

import fracture_plotter.utils.plot_routines as plot
from fracture_plotter.utils.general import get_paths


def create_places_and_methods_dict(refinement_indices, places_and_methods, paths):
    places_and_methods_dict = {k: places_and_methods.copy() for k in refinement_indices}

    for refinement_index in refinement_indices:
        for place, methods in places_and_methods.items():
            for method in methods:
                folder = os.path.join(paths.results_dir, place, method).replace(
                    r"\_", "_"
                )
                file_path = os.path.join(
                    folder, f"dot_refinement_{refinement_index}.csv"
                ).replace(r"\_", "_")
                if not os.path.exists(file_path):
                    del places_and_methods_dict[refinement_index][place]
                    break
    return places_and_methods_dict


def plot_data_over_time(places_and_methods, ref, ax, ID, title, fontsize=30):
    paths = get_paths(__file__)
    for place, methods in places_and_methods.items():
        for method in methods:
            folder = os.path.join(paths.results_dir, place, method).replace(r"\_", "_")
            data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace(r"\_", "_")
            label = place if place == "mean" else f"{place}-{method}"
            plot.plot_over_time(
                case=paths.case,
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
    refinement_indices=None,
    titles=None,
):
    paths = get_paths(__file__)
    if refinement_indices is None:
        refinement_indices = [0, 1, 2]
    if titles is None:
        titles = [f"Refinement {ref}" for ref in refinement_indices]

    for ID in range(8):
        fig, axes = plot.setup_figure(
            id_offset=ID, num_axes=len(refinement_indices), ylim=(-0.01, 1.01)
        )
        for title, ref, ax in zip(titles, refinement_indices, axes):
            places_and_methods_arg = plot.get_places_and_methods_arg(
                places_and_methods=places_and_methods, ref=ref
            )
            plot_data_over_time(
                places_and_methods=places_and_methods_arg,
                ref=ref,
                ax=ax,
                ID=ID,
                title=title,
                fontsize=fontsize,
            )
        plot.plot_legend_in_middle(fig=fig, ax1=axes[0], ax2=axes[1], fontsize=fontsize)
    plot.save_over_time(
        filename=f"pot",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )


if __name__ == "__main__":
    run_pot()
