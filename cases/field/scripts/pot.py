import os
import plotroutines as plot
import numpy as np

#------------------------------------------------------------------------------#
# add data to plots

# add plots for the different schemes
# The first argument is the path to your data, where the data is assumed to be ordered comma-separated in the following order:
#   -> 1. time
#      2. integral of \phi c within matrix sub-domain \Omega_3
#      3. integral of \phi c within fracture domain \Omega_f
#      4. outlux of the domain across the outfow boundary
# The second argument defines the legend you want to add to your data (Institution / Numerical method)
# The third argument specifies the plot id - use the ids defined in lines 35-37 for the different plots

# TODO: add reference solution to plots as soon as available

titles = ['$\\sim 30k$ cells', '$\\sim 150k$ cells']
refinement_index = ['0', '1', '2']
cond = 1

label = "USI"
place = "ETHZ\_USI"
method = "FEM\_LM"
ncol = 4

regions = [15, 45, 48]

for region_pos, region in enumerate(regions):
    title = "fracture " + str(region)
    fig = plot.plt.figure(plot.id_pot+11, figsize=(16, 6))
    fig.subplots_adjust(hspace=0, wspace=0)

    ax = fig.add_subplot(1, len(regions), region_pos + 1, ylim=(0-0.01, 1+0.01), xlim=(-100, 1800))

    for title, refinement in zip(titles, refinement_index):
            folder = "./cases/field/results/" 
            data = os.path.join(folder, f"dot_cond{cond}_{refinement}.csv")

            plot.plot_over_time(data, label, title, plot.id_pot, region, region_pos, len(regions), ax,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=False, fmt="%1.2f")


# save figures
plot.save_over_time("case_field_pot")

# ncol = 4
# for place in places_and_methods:
#     for method in places_and_methods[place]:
#         label = "\\texttt{" + place + "-" + method + "}"
#         plot.plot_legend(label, plot.id_pot_legend, plot.linestyle[place][method],
#                          plot.color[place][method], ncol)

# plot.save(plot.id_pot_legend, "case_field_pot_legend")
# plot.crop_pdf("case_field_pot_legend")

#------------------------------------------------------------------------------#
