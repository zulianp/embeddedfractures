import os

import plotroutines as plot

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

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dol_refinement_{ref}.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

            # Pass show_legend flag to the plot function
            plot.plot_over_line(
                filename=data,
                label=label,
                ref=ref,
                ID=plot.id_p_matrix,
                title=title,
                ax=axes_p_matrix,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                show_legend=show_legend,
                fontsize=fontsize,
            )

            if place != "DTU":  # Only pressure for DTU
                plot.plot_over_line(
                    filename=data,
                    label=label,
                    ref=ref,
                    ID=plot.id_c_matrix,
                    title=title,
                    ax=axes_c_matrix,
                    linestyle=plot.linestyle[place][method],
                    color=plot.color[place][method],
                    show_legend=show_legend,
                    fontsize=fontsize,
                )
                plot.plot_over_line(
                    filename=data,
                    label=label,
                    ref=ref,
                    ID=plot.id_c_fracture,
                    title=title,
                    ax=axes_c_fracture,
                    linestyle=plot.linestyle[place][method],
                    color=plot.color[place][method],
                    show_legend=show_legend,
                    fontsize=fontsize,
                )


def run_pol(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=12,
):
    paths = get_paths(__file__)

    titles = ["$\\sim 1k$ cells", "$\\sim 10k$ cells", "$\\sim 100k$ cells"]
    refinement_index = [0, 1, 2]

    # Setup figures and axes
    fig_p_matrix, axes_p_matrix_list = plot.setup_figure(
        plot.id_p_matrix, 3, ylim=(1 - 0.1, 4 + 0.1)
    )
    fig_c_matrix, axes_c_matrix_list = plot.setup_figure(
        plot.id_c_matrix, 3, ylim=(0 - 0.0005, 0.01 + 0.0005)
    )
    fig_c_fracture, axes_c_fracture_list = plot.setup_figure(
        plot.id_c_fracture, 3, ylim=(0.0075, 0.0101)
    )

    # Plot data
    for title, ref, idx, axes_p_matrix, axes_c_matrix, axes_c_fracture in zip(
        titles,
        refinement_index,
        range(3),
        axes_p_matrix_list,
        axes_c_matrix_list,
        axes_c_fracture_list,
    ):
        show_legend = (
            idx == 1
        )  # Show the legend only for the middle subplot (index 1, subfigure b)
        plot_data_over_lines(
            places_and_methods=places_and_methods,
            ref=ref,
            axes_p_matrix=axes_p_matrix,
            axes_c_matrix=axes_c_matrix,
            axes_c_fracture=axes_c_fracture,
            title=title,
            show_legend=show_legend,
            fontsize=fontsize,
        )

        # Add reference for USTUTT-MPFA
        ref_data = os.path.join(
            paths.results_dir, "USTUTT/MPFA/dol_refinement_5.csv".replace("\_", "_")
        )
        plot.plot_over_line(
            filename=ref_data,
            label="reference",
            ref=ref,
            ID=plot.id_p_matrix,
            title=title,
            ax=axes_p_matrix,
            linestyle=plot.linestyle["USTUTT"]["reference"],
            color=plot.color["USTUTT"]["reference"],
            fontsize=fontsize,
            show_legend=show_legend,
        )

        # Only add the legend to the middle subplot (subfigure b)
        if idx == 1:
            plot.plot_legend_in_middle(ax=axes_p_matrix, fontsize=fontsize)
            plot.plot_legend_in_middle(ax=axes_c_matrix, fontsize=fontsize)
            plot.plot_legend_in_middle(ax=axes_c_fracture, fontsize=fontsize)

    # Save figures with integrated legends
    plot.save(
        ID=plot.id_p_matrix,
        filename=f"{paths.case}_pol_p_matrix",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )
    plot.save(
        ID=plot.id_c_matrix,
        filename=f"{paths.case}_pol_c_matrix",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )
    plot.save(
        ID=plot.id_c_fracture,
        filename=f"{paths.case}_pol_c_fracture",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )


if __name__ == "__main__":
    run_pol()
