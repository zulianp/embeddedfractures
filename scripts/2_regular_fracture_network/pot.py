# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import numpy as np
import plotroutines as plot

def run_pot():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    results_dir = curr_dir.replace("scripts", "results")
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    titles = ['$\\sim 4k$ cells  - permeability 1e4', '$\\sim 4k$ cells  - permeability 1e-4']
    conds = [1]

    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    # TODO: Verify with Arancia
    # regions = np.array([1, 10, 11])
    # regions_fig = {1: f"{case}_region10pic.png", 10: f"{case}_region11pic.png", 11: f"{case}_region1pic.png"}

    regions = np.array([1])
    regions_fig = {1: f"{case}_region10pic.png"}

    #------------------------------------------------------------------------------#

    for cond, title in zip(conds, titles):

        fig = plot.plt.figure(cond+11, figsize=(16, 6))
        fig.subplots_adjust(hspace=0, wspace=0)
        if cond == 0:
            ylim = (0, 0.475)
        else:
            ylim = (0, 0.4)

        for region_pos, region in enumerate(regions):
            ax = fig.add_subplot(1, regions.size, region_pos + 1, ylim=ylim)

            for place in places_and_methods:
                for method in places_and_methods[place]:
                    folder = os.path.join(results_dir, place, method)
                    data = os.path.join(folder, f"dot_cond_{cond}.csv").replace("\_", "_")
                    label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

                    if place.replace("\_", "_") != "mean":
                        plot.plot_over_time(data, label, title, cond, region, region_pos, regions.size, ax,
                                            linestyle=plot.linestyle[place][method],
                                            color=plot.color[place][method],
                                            has_legend=False, fmt="%1.2f")
                    else:
                        std_data = data.replace("mean", "std")
                        plot.plot_mean_and_std_over_time(data, std_data, label, title, cond, region, region_pos, regions.size, ax,
                                                        linestyle=plot.linestyle[place][method],
                                                        color=plot.color[place][method],
                                                        has_legend=False, fmt="%1.2f")

        # save figures
        plot.save(cond, f"{case}_cot_cond_{cond}", starting_from=3*cond)

    ncol = 4
    for cond in conds:
        for place in places_and_methods:
            for method in places_and_methods[place]:
                label = "\\texttt{" + place + ("-" + method if place.replace("\_", "_") != "mean" else "") + "}"
                plot.plot_legend(label, cond, plot.linestyle[place][method],
                                 plot.color[place][method], ncol)

        plot.save(cond, f"{case}_cot_cond_{cond}_legend")
        plot.crop_pdf(f"{case}_cot_cond_{cond}_legend")


if __name__ == "__main__":
    run_pot()
