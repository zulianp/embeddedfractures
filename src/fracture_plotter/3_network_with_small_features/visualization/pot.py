import os

import plotroutines as plot

from fracture_plotter.utils.general import get_paths


def plot_data_over_time(places_and_methods, ref, ax, ID, title):
    paths = get_paths(__file__)

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace("\_", "_")
            label = place + ("-" + method if place != "mean" else "")

            plot.plot_over_time(
                data,
                label,
                ref,
                ID,
                title,
                ax,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                has_legend=False,
            )


def run_pot(places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]}):
    paths = get_paths(__file__)

    titles = ["$\\sim 30k$ cells", "$\\sim 150k$ cells"]
    refinement_index = ["0", "1"]

    # Iterate over 8 IDs
    for ID in range(8):
        # Set up the figure and axes using the provided function
        fig, axes = plot.setup_figure(
            ID, 2, ylim=(0 - 0.01, 1 + 0.01)
        )  # Using correct ylim

        # Plot data for each refinement level
        for title, ref, ax in zip(titles, refinement_index, axes):
            plot_data_over_time(places_and_methods, ref, ax, ID, title)

        # Add a single legend below the two subplots
        plot.plot_legend_in_middle(fig, axes[0], axes[1])

    # Save the time-based plots for all fractures
    plot.save_over_time(f"{paths.case}_pot")


if __name__ == "__main__":
    run_pot()
