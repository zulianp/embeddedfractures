import os
import plotroutines as plot

#------------------------------------------------------------------------------#
# Insert here your data for the plotting, see the file 'color_regions.vtu'
# for the coloring code of each region.

titles = ['$\\sim 500$ cells', '$\\sim 4k$ cells', '$\\sim 32k$ cells']
refinement_index = [0, 1, 2]
conds = [1]

places_and_methods = {
    "ETHZ\_USI": ["FEM\_LM"],
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
                folder = "../results/"
                data = os.path.join(folder, f"dol_cond{cond}_{ref}.csv")
                label = f"{place}_{method}"

                # Check if the file exists at the constructed path
                if not os.path.isfile(data):
                    print(f"Error: Data file '{data}' not found.")
                    exit(0)
                else:
                    plot.plot_over_line(data, label, ref, title, cond, ax,
                                        plot.linestyle[place][method], plot.color[place][method],
                                        has_legend=False, fmt=fmt)

        # TODO: Ask Patrick if we would still like this reference or not.
        # add reference (4th refinement of USTUTT-MPFA)
        # place = "USTUTT"
        # method = "reference"
        # label = "reference"
        # data = "../results/USTUTT/MPFA/dol_cond_" + str(cond) + "_refinement_4.csv"
        # plot.plot_over_line(data, label, ref, title, cond, ax,
        #                     plot.linestyle[place][method], plot.color[place][method],
        #                     has_legend=False, fmt=fmt)

    # save figures
    plot.save(cond, "case2_pol_cond"+str(cond), starting_from=3*cond)

ncol = 4
for cond in conds:
    for place in places_and_methods:
        for method in places_and_methods[place]:
            label = "\\texttt{" + place + "-" + method + "}"
            plot.plot_legend(label, cond, plot.linestyle[place][method],
                             plot.color[place][method], ncol)

    # add reference to legend
    # plot.plot_legend("reference", cond, plot.linestyle["USTUTT"]["reference"],
    #                  plot.color["USTUTT"]["reference"], ncol)

    plot.save(cond, f"case2_pol_cond{cond}_legend")
    plot.crop_pdf(f"case2_pol_cond{cond}_legend")

#------------------------------------------------------------------------------#
