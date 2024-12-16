import os
import plotroutines as plot
from scripts.utils.general import get_paths
curr_dir = os.path.dirname(os.path.abspath(__file__))
case = curr_dir.split(os.sep)[-1]  # case we are dealing with
plots_dir, results_dir = get_paths(curr_dir)

def plot_data_over_time(places_and_methods, ax, title, region, region_pos, num_regions, show_legend=False):
    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method)
            data = os.path.join(folder, "dot.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")
            plot.plot_over_time(data, label, title, plot.id_pot, region, region_pos, num_regions, ax,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=show_legend, fmt="%1.2f")

def run_pot(places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]}):
    # Fracture regions and axis limits
    regions = [15, 45, 48]
    ylim = (0 - 0.01, 1 + 0.01)
    xlim = (-100, 1800)

    # Create figure for plotting
    fig = plot.plt.figure(plot.id_pot + 11, figsize=(16, 6))
    fig.subplots_adjust(hspace=0, wspace=0)

    # Plot data for each region
    for region_pos, region in enumerate(regions):
        title = f"fracture {region}"
        ax = fig.add_subplot(1, len(regions), region_pos + 1, ylim=ylim, xlim=xlim)
        show_legend = (region_pos == 1)  # Show the legend only for the middle subplot
        plot_data_over_time(places_and_methods, ax, title, region, region_pos, len(regions), show_legend)

        # Add the legend to the middle subplot
        if region_pos == 1:
            plot.plot_legend_in_middle(ax)

    # Save the figure with the integrated legend
    plot.save(plot.id_pot, f"{case}_pot")


if __name__ == "__main__":
    run_pot()
