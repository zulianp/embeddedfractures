import os
import plotroutines as plot
import numpy as np

def plot_data_over_time(places_and_methods, results_dir, ref, ax, ID, title):
    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace("\_", "_")
            label = place + ("-" + method if place != "mean" else "")

            plot.plot_over_time(data, label, ref, ID, title, ax,
                                linestyle=plot.linestyle[place][method], color=plot.color[place][method],
                                has_legend=False)

def run_pot():
    curr_dir = os.path.dirname(os.path.realpath(__file__))  # current directory
    results_dir = curr_dir.replace('scripts', 'results')
    case = curr_dir.split(os.sep)[-1]  # case we are dealing with
    titles = ['$\\sim 30k$ cells', '$\\sim 150k$ cells']
    refinement_index = ['0', '1']
    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    # Iterate over 8 IDs
    for ID in range(8):
        # Setup the figure and axes using the provided function
        fig, axes = plot.setup_figure(ID, 2, ylim=(0 - 0.01, 1 + 0.01))  # Using correct ylim

        # Plot data for each refinement level
        for title, ref, ax in zip(titles, refinement_index, axes):
            plot_data_over_time(places_and_methods, results_dir, ref, ax, ID, title)

        # Add a single legend below the two subplots
        plot.plot_legend_in_middle(fig, axes[0], axes[1])

    # Save the time-based plots for all fractures
    plot.save_over_time(f"{case}_pot")

if __name__ == "__main__":
    run_pot()