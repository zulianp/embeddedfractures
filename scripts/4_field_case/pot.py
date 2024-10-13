# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import numpy as np
import plotroutines as plot

def run_pot():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    results_dir = curr_dir.replace('scripts', 'results')
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    title = ""
    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    regions = [15, 45, 48]
    for region_pos, region in enumerate(regions):
        title = "fracture " + str(region)
        fig = plot.plt.figure(plot.id_pot+11, figsize=(16, 6))
        fig.subplots_adjust(hspace=0, wspace=0)

        ax = fig.add_subplot(1, len(regions), region_pos + 1, ylim=(0-0.01, 1+0.01), xlim=(-100, 1800))

        for place in places_and_methods:
            for method in places_and_methods[place]:
                folder = os.path.join(results_dir, place, method)
                data = os.path.join(folder, "dot.csv").replace("\_", "_")
                label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

                plot.plot_over_time(data, label, title, plot.id_pot, region, region_pos, len(regions), ax,
                                    plot.linestyle[place][method], plot.color[place][method],
                                    has_legend=False, fmt="%1.2f")
    # save figures
    plot.save(plot.id_pot, f"{case}_pot")

    ncol = 4
    for place in places_and_methods:
        for method in places_and_methods[place]:
            label = "\\texttt{" + place + ("-" + method if place.replace("\_", "_") != "mean" else "") + "}"
            plot.plot_legend(label, plot.id_pot_legend, plot.linestyle[place][method],
                             plot.color[place][method], ncol)

    plot.save(plot.id_pot_legend, f"{case}_pot_legend")
    plot.crop_pdf(f"{case}_pot_legend")


if __name__ == "__main__":
    run_pot()