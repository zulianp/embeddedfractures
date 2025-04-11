import os

import fracture_plotter.utils.plot_routines as plot
from fracture_plotter.utils.general import get_paths


def plot_data_over_lines(
    places_and_methods,
    ref,
    axes_p_matrix,
    axes_c_matrix,
    axes_c_fracture,
    title,
    show_legend=False,
    fontsize=30,
):
    paths = get_paths(__file__)
    for place, methods in places_and_methods.items():
        for method in methods:
            folder = os.path.join(paths.results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dol_refinement_{ref}.csv").replace("\_", "_")
            label = place if place == "mean" else f"{place}-{method}"
            common = {
                "filename": data,
                "label": label,
                "ref": ref,
                "title": title,
                "linestyle": plot.linestyle[place][method],
                "color": plot.color[place][method],
                "show_legend": show_legend,
                "fontsize": fontsize,
            }
            plot.plot_over_line(
                case=paths.case, ID=plot.id_p_matrix, ax=axes_p_matrix, **common
            )
            if place != "DTU":
                for ID, ax in (
                    (plot.id_c_matrix, axes_c_matrix),
                    (plot.id_c_fracture, axes_c_fracture),
                ):
                    plot.plot_over_line(case=paths.case, ID=ID, ax=ax, **common)


def run_pol(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=12,
    refinement_index=None,
    titles=None,
):
    paths = get_paths(__file__)
    if refinement_index is None:
        refinement_index = [0, 1, 2]
    if titles is None:
        titles = [f"Refinement {ref}" for ref in refinement_index]

    fig_p_matrix, axes_p_matrix_list = plot.setup_figure(
        id_offset=plot.id_p_matrix, num_axes=len(refinement_index), ylim=(0.9, 4.1)
    )
    fig_c_matrix, axes_c_matrix_list = plot.setup_figure(
        id_offset=plot.id_c_matrix,
        num_axes=len(refinement_index),
        ylim=(-0.0005, 0.0105),
    )
    fig_c_fracture, axes_c_fracture_list = plot.setup_figure(
        id_offset=plot.id_c_fracture,
        num_axes=len(refinement_index),
        ylim=(0.0075, 0.0101),
    )

    for idx, (title, ref, ax_p, ax_c, ax_cf) in enumerate(
        zip(
            titles,
            refinement_index,
            axes_p_matrix_list,
            axes_c_matrix_list,
            axes_c_fracture_list,
        )
    ):
        show_legend = idx == 1
        plot_data_over_lines(
            places_and_methods=places_and_methods,
            ref=ref,
            axes_p_matrix=ax_p,
            axes_c_matrix=ax_c,
            axes_c_fracture=ax_cf,
            title=title,
            show_legend=show_legend,
            fontsize=fontsize,
        )

        ref_data = os.path.join(
            paths.results_dir, "USTUTT/MPFA/dol_refinement_5.csv".replace("\_", "_")
        )
        ref_common = {
            "filename": ref_data,
            "label": "reference",
            "ref": ref,
            "title": title,
            "linestyle": plot.linestyle["USTUTT"]["reference"],
            "color": plot.color["USTUTT"]["reference"],
            "fontsize": fontsize,
            "show_legend": show_legend,
        }
        plot.plot_over_line(case=paths.case, ID=plot.id_p_matrix, ax=ax_p, **ref_common)
        if show_legend:
            for ax in (ax_p, ax_c, ax_cf):
                plot.plot_legend_in_middle(ax=ax, fontsize=fontsize)

    for ID, suffix in (
        (plot.id_p_matrix, "pol_p_matrix"),
        (plot.id_c_matrix, "pol_c_matrix"),
        (plot.id_c_fracture, "pol_c_fracture"),
    ):
        plot.save(
            ID=ID,
            filename=suffix,
            plots_dir=paths.plots_dir,
            fontsize=subfig_fontsize,
        )


if __name__ == "__main__":
    run_pol()
