import os
import numpy as np
import plotroutines as plot

#------------------------------------------------------------------------------#

# Insert here your data for the plotting, see the file 'color_regions.vtu'
# for the coloring code of each region.

titles = ['$\\sim 4k$ cells  - permeability 1e4', '$\\sim 4k$ cells  - permeability 1e-4']
regions = np.array([1, 10, 11])
regions_fig = {1: "case2_region10pic.png", 10: "case2_region11pic.png", 11: "case2_region1pic.png"}
cond = 1
num_regions = 22

#------------------------------------------------------------------------------#

for title in titles:

    fig = plot.plt.figure(cond+11, figsize=(16, 6))
    fig.subplots_adjust(hspace=0, wspace=0)
    ylim = (0, 0.4)

    for region_pos, region in enumerate(regions):
        ax = fig.add_subplot(1, regions.size, region_pos + 1, ylim=ylim)

        folder = "../results/" 
        data = os.path.join(folder, "dot_cond1_0.csv")

        plot.plot_over_time(file_name=data, title=title, region_pos=region_pos, num_regions=num_regions, ax=ax, clr="blue", has_legend=False, fmt="%1.2f")

    # save figures
    plot.save(1, "case2_cot_cond1", starting_from=3*cond)