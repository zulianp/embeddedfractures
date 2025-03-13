import os

import plotroutines as plot


def run_percentiles(places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]}):
    paths = plot.get_paths(__file__)

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

    # Plot percentiles for each refinement level
    for ref, idx, axes_p_matrix, axes_c_matrix, axes_c_fracture in zip(
        ["0", "1", "2"],
        range(3),
        axes_p_matrix_list,
        axes_c_matrix_list,
        axes_c_fracture_list,
    ):
        plot.plot_percentiles(ref, plot.id_p_matrix, places_and_methods, axes_p_matrix)
        plot.plot_percentiles(ref, plot.id_c_matrix, places_and_methods, axes_c_matrix)
        plot.plot_percentiles(
            ref, plot.id_c_fracture, places_and_methods, axes_c_fracture
        )

    # Save figures
    plot.save(
        plot.id_p_matrix, f"{paths.case}_pol_p_matrix_percentile_90_10", starting_from=3
    )
    plot.save(
        plot.id_c_matrix, f"{paths.case}_pol_c_matrix_percentile_90_10", starting_from=3
    )
    plot.save(
        plot.id_c_fracture,
        f"{paths.case}_pol_c_fracture_percentile_90_10",
        starting_from=3,
    )


if __name__ == "__main__":
    run_percentiles()
