import os

import plotroutines as plot


def run_percentiles(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=12,
):
    paths = plot.get_paths(__file__)
    config = [
        (plot.id_p_matrix, (0.9, 4.1), f"{paths.case}_pol_p_matrix_percentile_90_10"),
        (
            plot.id_c_matrix,
            (-0.0005, 0.0105),
            f"{paths.case}_pol_c_matrix_percentile_90_10",
        ),
        (
            plot.id_c_fracture,
            (0.0075, 0.0101),
            f"{paths.case}_pol_c_fracture_percentile_90_10",
        ),
    ]

    # Setup figures and axes for all IDs
    axes_lists = [plot.setup_figure(ID, 3, ylim=ylim)[1] for ID, ylim, _ in config]

    # Plot percentiles for each refinement level in parallel axes
    for ref, axes in zip(["0", "1", "2"], zip(*axes_lists)):
        for (ID, _, _), ax in zip(config, axes):
            plot.plot_percentiles(
                ref=ref,
                ID=ID,
                places_and_methods=places_and_methods,
                ax=ax,
                fontsize=fontsize,
            )

    # Save figures
    for ID, _, filename in config:
        plot.save(
            ID,
            filename,
            starting_from=3,
            plots_dir=paths.plots_dir,
            fontsize=subfig_fontsize,
        )


if __name__ == "__main__":
    run_percentiles()
