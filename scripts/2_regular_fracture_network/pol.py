# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os
import plotroutines as plot

def run_pol():
    curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
    results_dir = curr_dir.replace("scripts", "results")
    case = curr_dir.split(os.sep)[-1] # case we are dealing with
    titles = ['$\\sim 500$ cells', '$\\sim 4k$ cells', '$\\sim 32k$ cells']
    refinement_index = [0, 1, 2]
    conds = [1]
    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    for cond in conds:
        fig = plot.plt.figure(cond+11, figsize=(16, 6))
        fig.subplots_adjust(hspace=0, wspace=0)
        if cond == 0:
            ylim = (0.5, 2.75)
            fmt = "%1.2f"
        else:
            ylim = (0.4, 5.75)
            fmt = "%1.2e"

        for title, ref in zip(titles, refinement_index):

            ax = fig.add_subplot(1, 3, ref + 1, ylim=ylim)

            for place in places_and_methods:
                for method in places_and_methods[place]:
                    folder = os.path.join(results_dir, place, method).replace("\_", "_")
                    data = os.path.join(folder, f"dol_cond_{cond}_refinement_{ref}.csv").replace("\_", "_")
                    label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")

                    if place.replace("\_", "_") != "mean":
                        plot.plot_over_line(data, label, ref, title, cond, ax,
                                            plot.linestyle[place][method], plot.color[place][method],
                                            has_legend=False, fmt=fmt)
                    else:
                        std_data = data.replace("mean", "std")
                        plot.plot_mean_and_std_over_line(data, std_data, label, ref, title, cond, ax,
                                                        plot.linestyle[place][method], plot.color[place][method],
                                                        has_legend=False, fmt=fmt)

            # Add reference (4th refinement of USTUTT-MPFA)
            place = "USTUTT"
            method = "reference"
            label = "reference"
            data = os.path.join(results_dir, f"USTUTT/MPFA/dol_cond_{cond}_refinement_4.csv")
            plot.plot_over_line(data, label, ref, title, cond, ax,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=False, fmt=fmt)

        # Save figures
        plot.save(cond, f"{case}_pol_cond_{cond}", starting_from=3*cond)

    ncol = 4
    for cond in conds:
        for place in places_and_methods:
            for method in places_and_methods[place]:
                label = "\\texttt{" + place + ("-" + method if place.replace("\_", "_") != "mean" else "") + "}"
                plot.plot_legend(label, cond, plot.linestyle[place][method],
                                 plot.color[place][method], ncol)

        # Add reference to legend
        plot.plot_legend("reference", cond, plot.linestyle["USTUTT"]["reference"],
                         plot.color["USTUTT"]["reference"], ncol)

        plot.save(cond, f"{case}_pol_cond_{cond}_legend")
        plot.crop_pdf(f"{case}_pol_cond_{cond}_legend")
