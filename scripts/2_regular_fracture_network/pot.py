import os
import numpy as np
import plotroutines as plot

def plot_cond_over_time(places_and_methods, results_dir, cond, ax, title, region, region_pos, num_regions, ylim, show_legend=False):
    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method)
            data_file = os.path.join(folder, f"dot_cond_{cond}.csv").replace("\\_",  "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

            plot.plot_over_time(data_file, label, title, cond, region, region_pos, num_regions, ax,
                                linestyle=plot.linestyle[place][method], color=plot.color[place][method],
                                has_legend=show_legend, ylim=ylim)

def run_pot():
    curr_dir, plots_dir, results_dir, _ = plot.get_paths()
    case = curr_dir.split(os.sep)[-1]
    titles = ['$\\sim 4k$ cells - permeability 1e4', '$\\sim 4k$ cells - permeability 1e-4']
    conds = [1]  # List of conditions
    places_and_methods = {"USI": ["FEM\_LM"], "mean": ["key"]}
    regions = [1]  # Single region for this case

    # Setup figures and axes for each condition and region
    for cond, title in zip(conds, titles):
        fig, axes_list = plot.setup_figure(cond, len(regions), ylim=(0, 0.4 if cond else 0.475))

        for region_pos, region in enumerate(regions):
            ax = axes_list[region_pos]
            show_legend = True  # Ensure the legend is shown in this case
            plot_cond_over_time(places_and_methods, results_dir, cond, ax, title, region, region_pos, len(regions),
                                ylim=(0, 0.4 if cond else 0.475), show_legend=show_legend)

            # Add the legend directly to the figure (on the first region)
            if region_pos == 0:  # or region_pos == 1 for middle
                plot.plot_legend_in_middle(ax)

        # Save figure without creating a separate legend file
        plot.save(cond, f"{case}_cot_cond_{cond}", starting_from=3 * cond)

if __name__ == "__main__":
    run_pot()
