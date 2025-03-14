import os

import plotroutines as plot

from fracture_plotter.utils.general import get_paths


def plot_data_over_lines(
    places_and_methods,
    ref,
    axes_p_0,
    axes_p_1,
    title,
    show_legend=False,
    show_title=True,
):
    paths = get_paths(__file__)

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method).replace("\_", "_")
            label = place + ("-" + method if place != "mean" else "")

            # Plot data for line 0
            data_0 = os.path.join(folder, f"dol_line_0_refinement_{ref}.csv").replace(
                "\_", "_"
            )
            plot.plot_over_line(
                file_name=data_0,
                label=label,
                simulation_id=ref,
                cond=plot.id_p_0_matrix,
                title=title,
                ax=axes_p_0,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                has_legend=show_legend,
                has_title=show_title,
            )

            # Plot data for line 1
            data_1 = os.path.join(folder, f"dol_line_1_refinement_{ref}.csv").replace(
                "\_", "_"
            )
            plot.plot_over_line(
                file_name=data_1,
                label=label,
                simulation_id=ref,
                cond=plot.id_p_1_matrix,
                title=title,
                ax=axes_p_1,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                has_legend=show_legend,
                has_title=show_title,
            )


def run_pol(places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]}):
    paths = get_paths(__file__)

    titles = ["$\\sim 30k$ cells", "$\\sim 150k$ cells"]
    refinement_index = [0, 1]

    # Setup figures and axes
    fig_p_0, axes_p_0_list = plot.setup_figure(
        plot.id_p_0_matrix, 2, ylim=(0.025, 0.08)
    )
    fig_p_1, axes_p_1_list = plot.setup_figure(
        plot.id_p_1_matrix, 2, ylim=(0.02, 0.075)
    )

    # Plot data
    show_title = True
    for title, ref, idx, axes_p_0, axes_p_1 in zip(
        titles, refinement_index, range(2), axes_p_0_list, axes_p_1_list
    ):
        show_legend = idx == 0  # Show legend only for the first subplot
        plot_data_over_lines(
            places_and_methods, ref, axes_p_0, axes_p_1, title, show_legend, show_title
        )

        # Add reference for USTUTT-MPFA
        ref_folder = os.path.join(paths.results_dir, "USTUTT", "MPFA")
        ref_data_0 = os.path.join(ref_folder, "dol_line_0_refinement_5.csv")
        ref_data_1 = os.path.join(ref_folder, "dol_line_1_refinement_5.csv")
        plot.plot_over_line(
            file_name=ref_data_0,
            label="reference",
            simulation_id=ref,
            cond=plot.id_p_0_matrix,
            title=title,
            ax=axes_p_0,
            linestyle=plot.linestyle["USTUTT"]["reference"],
            color=plot.color["USTUTT"]["reference"],
            has_legend=show_legend,
            has_title=show_title,
        )
        plot.plot_over_line(
            file_name=ref_data_1,
            label="reference",
            simulation_id=ref,
            cond=plot.id_p_1_matrix,
            title=title,
            ax=axes_p_1,
            linestyle=plot.linestyle["USTUTT"]["reference"],
            color=plot.color["USTUTT"]["reference"],
            has_legend=show_legend,
            has_title=show_title,
        )

        # Add the legend to the middle subplot (subfigure b)
        if idx == 1:
            plot.plot_legend_in_middle(fig_p_0, axes_p_0, axes_p_1)
            plot.plot_legend_in_middle(fig_p_1, axes_p_0, axes_p_1)

    # Save figures
    plot.save(plot.id_p_0_matrix, f"{paths.case}_pol_p_line_0")
    plot.save(plot.id_p_1_matrix, f"{paths.case}_pol_p_line_1")


if __name__ == "__main__":
    run_pol()
