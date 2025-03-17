import os

import plotroutines as plot

from fracture_plotter.utils.general import get_paths


def plot_data_over_time(
    places_and_methods,
    ax,
    title,
    region,
    region_pos,
    fontsize=30,
    show_legend=False,
):
    paths = get_paths(__file__)

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method)
            data = os.path.join(folder, "dot.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")
            plot.plot_over_time(
                filename=data,
                label=label,
                title=title,
                region=region,
                region_pos=region_pos,
                ax=ax,
                linestyle=plot.linestyle[place][method],
                color=plot.color[place][method],
                fontsize=fontsize,
                show_legend=show_legend,
            )


def run_pot(
    places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]},
    fontsize=30,
    subfig_fontsize=25,
):
    paths = get_paths(__file__)

    # Fracture regions and axis limits
    regions = [15, 45, 48]
    ylim = (0 - 0.01, 1 + 0.01)
    xlim = (-100, 1800)

    # Create figure for plotting
    fig, axes_list = plot.setup_figure(
        id_offset=plot.id_pot, num_axes=len(regions), xlim=xlim, ylim=ylim
    )

    # Plot data for each region
    for region_pos, region in enumerate(regions):
        ax = axes_list[region_pos]
        title = f"fracture {region}"
        show_legend = region_pos == 1  # Show the legend only for the middle subplot

        plot_data_over_time(
            places_and_methods=places_and_methods,
            ax=ax,
            title=title,
            region=region,
            region_pos=region_pos,
            fontsize=fontsize,
            show_legend=show_legend,
        )

        # Add the legend to the middle subplot
        if region_pos == 1:
            plot.plot_legend_in_middle(ax=ax, fontsize=fontsize)

    # Save the figure with the integrated legend
    plot.save(
        ID=plot.id_pot,
        filename=f"{paths.case}_pot",
        plots_dir=paths.plots_dir,
        fontsize=subfig_fontsize,
    )


if __name__ == "__main__":
    run_pot()
