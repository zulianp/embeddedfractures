import os

import fracture_plotter.utils.plot_routines as plot
from fracture_plotter.utils.general import get_paths


def plot_data_over_lines(
    places_and_methods,
    ref,
    ax0,
    ax1,
    title,
    show_legend=False,
    show_title=True,
    fontsize=30,
):
    paths = get_paths(__file__)
    for place, methods in places_and_methods.items():
        for method in methods:
            folder = os.path.join(paths.results_dir, place, method).replace(r"\_", "_")
            label = place if place == "mean" else f"{place}-{method}"
            for line, cond, ax in (
                (0, plot.id_p_0_matrix, ax0),
                (1, plot.id_p_1_matrix, ax1),
            ):
                data = os.path.join(
                    folder, f"dol_line_{line}_refinement_{ref}.csv"
                ).replace(r"\_", "_")
                
                plot.plot_over_line(
                    case=paths.case,
                    filename=data,
                    label=label,
                    ref=ref,
                    title=title,
                    ax=ax,
                    linestyle=plot.linestyle[place][method],
                    color=plot.color[place][method],
                    fontsize=fontsize,
                    show_legend=show_legend,
                    show_title=show_title,
                )


def run_pol(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=25,
    refinement_index=None,
    titles=None,
):
    paths = get_paths(__file__)
    if refinement_index is None:
        refinement_index = [0, 1, 2]
    if titles is None:
        titles = [f"Refinement {ref}" for ref in refinement_index]

    fig0, axes0 = plot.setup_figure(
        id_offset=plot.id_p_0_matrix, num_axes=len(refinement_index), ylim=(0.025, 0.08)
    )
    fig1, axes1 = plot.setup_figure(
        id_offset=plot.id_p_1_matrix, num_axes=len(refinement_index), ylim=(0.02, 0.075)
    )

    mid_index = len(refinement_index) // 2
    for idx, (title, ref) in enumerate(zip(titles, refinement_index)):
        show_legend = idx == mid_index
        ax0_current, ax1_current = axes0[idx], axes1[idx]
        plot_data_over_lines(
            places_and_methods, ref, ax0_current, ax1_current, title, show_legend, True
        )

        # Plot reference data for USTUTT-MPFA
        ref_folder = os.path.join(paths.results_dir, "USTUTT", "MPFA")
        for line, cond, ax in (
            (0, plot.id_p_0_matrix, ax0_current),
            (1, plot.id_p_1_matrix, ax1_current),
        ):
            ref_data = os.path.join(ref_folder, f"dol_line_{line}_refinement_5.csv")
            plot.plot_over_line(
                case=paths.case,
                filename=ref_data,
                label="reference",
                ref=ref,
                title=title,
                ax=ax,
                linestyle=plot.linestyle["USTUTT"]["reference"],
                color=plot.color["USTUTT"]["reference"],
                fontsize=fontsize,
                show_legend=show_legend,
                show_title=True,
            )

        if idx == mid_index:
            plot.plot_legend_in_middle(fig=fig0, ax1=ax0_current, ax2=ax1_current)
            plot.plot_legend_in_middle(fig=fig1, ax1=ax0_current, ax2=ax1_current)

    plot.save(
        ID=plot.id_p_0_matrix,
        filename=f"pol_p_line_0",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )
    plot.save(
        ID=plot.id_p_1_matrix,
        filename=f"pol_p_line_1",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )


if __name__ == "__main__":
    run_pol()
