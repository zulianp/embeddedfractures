import os
import plotroutines as plot

#------------------------------------------------------------------------------#
# Insert here your data for the plotting, see the file 'color_regions.vtu'
# for the coloring code of each region.

titles = ['$\\sim 500$ cells', '$\\sim 4k$ cells', '$\\sim 32k$ cells']
refinement_index = [0, 1, 2]
cond = 1


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

    folder = "./cases/regular/results/"
    data = os.path.join(folder, f"dol_cond{cond}_{ref}.csv")

    # Check if the file exists at the constructed path
    if not os.path.isfile(data):
        print(f"Error: Data file '{data}' not found.")
        exit(0)
    else:
        plot.plot_over_line(file_name=data, simulation_id=ref, title=title, ax=ax, has_legend=False, fmt=fmt)
# save figures
plot.save(cond, "case2_pol_cond"+str(cond))
