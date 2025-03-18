import os

import fracture_plotter.utils.plot_routines as plot
from fracture_plotter.utils.general import get_paths


def plot_data_over_lines(
    places_and_methods, ref, ax, title, cond, show_legend=False, fontsize=30
):
    paths = get_paths(__file__)
    for place, methods in places_and_methods.items():
        for method in methods:
            folder = os.path.join(paths.results_dir, place, method).replace("\_", "_")
            data = os.path.join(
                folder, f"dol_cond_{cond}_refinement_{ref}.csv"
            ).replace("\_", "_")
            label = place if place == "mean" else f"{place}-{method}"
            plot.plot_over_line(
                case=paths.case_num,
                filename=data,
                label=label,
                ref=ref,
                title=title,
                ax=ax,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                show_legend=show_legend,
                fontsize=fontsize,
            )
    ref_data = os.path.join(
        paths.results_dir,
        f"USTUTT/MPFA/dol_cond_{cond}_refinement_4.csv".replace("\_", "_"),
    )
    plot.plot_over_line(
        case=paths.case_num,
        filename=ref_data,
        label="reference",
        ref=ref,
        title=title,
        ax=ax,
        linestyle=plot.linestyle["USTUTT"]["reference"],
        color=plot.color["USTUTT"]["reference"],
        show_legend=show_legend,
        fontsize=fontsize,
    )


def run_pol(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=24,
):
    paths = get_paths(__file__)
    titles = ["$\\sim 500$ cells", "$\\sim 4k$ cells", "$\\sim 32k$ cells"]
    refinement_indices = [0, 1, 2]
    cond, fmt = 0, {0: "%1.2f", 1: "%1.2e"}.get(0)
    ylim = {0: (0.5, 2.75), 1: (0.4, 5.75)}.get(cond)
    fig, axes_list = plot.setup_figure(
        id_offset=cond, num_axes=len(refinement_indices), ylim=ylim
    )

    for idx, (title, ref, ax) in enumerate(zip(titles, refinement_indices, axes_list)):
        show_legend = idx == 1
        plot_data_over_lines(
            places_and_methods=places_and_methods,
            ref=ref,
            ax=ax,
            title=title,
            cond=cond,
            show_legend=show_legend,
            fontsize=fontsize,
        )
        if idx == 1:
            plot.plot_legend_in_middle(ax=ax, fontsize=fontsize)

    plot.save(
        ID=cond,
        filename=f"{paths.case}_pol_cond_{cond}",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )
    plot.crop_pdf(
        f"{paths.case}_pol_cond_{cond}_legend",
        plots_dir=paths.plots_dir,
    )


if __name__ == "__main__":
    run_pol()
