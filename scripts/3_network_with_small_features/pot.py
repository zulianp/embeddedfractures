# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import plotroutines as plot
import numpy as np

def run_pot():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    results_dir = curr_dir.replace('scripts', 'results')
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    titles = ['$\\sim 30k$ cells', '$\\sim 150k$ cells']
    refinement_index = ['0', '1']

    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    for ID in np.arange(8):

        fig = plot.plt.figure(ID+11, figsize=(16, 6))
        fig.subplots_adjust(hspace=0, wspace=0)

        for title, ref in zip(titles, refinement_index):

            ax = fig.add_subplot(1, 2, int(ref) + 1, ylim=((0-0.01, 1+0.01)))

            for place in places_and_methods:
                for method in places_and_methods[place]:
                    folder = os.path.join(results_dir, place, method)
                    data = os.path.join(folder, f"dot_refinement_{ref}.csv").replace("\_", "_")
                    label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

                    if place.replace("\_", "_") != "mean":
                        plot.plot_over_time(data, label, ref, ID, title, ax,
                                            linestyle=plot.linestyle[place][method], color=plot.color[place][method],
                                            has_legend=False)
                    else:
                        std_data = data.replace("mean", "std")
                        plot.plot_mean_and_std_over_time(data, std_data, label, ref, ID, title, ax,
                                                        linestyle=plot.linestyle[place][method], color=plot.color[place][method],
                                                        has_legend=False)

    # save figures
    plot.save_over_time(f"{case}_pot")

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
