import os
import numpy as np
import plotroutines as plot

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

titles = np.array(['$\\sim 1k$ cells', '$\\sim 10k$ cells', '$\\sim 100k$ cells'])
refinement_index = np.array(['0', '1', '2'])
cond = 1

label = "USI"
place = "ETHZ\_USI"
method = "FEM\_LM"
ncol = 4

fig_intc_matrix = plot.plt.figure(plot.id_intc_matrix+11, figsize=(16, 6))
fig_intc_matrix.subplots_adjust(hspace=0, wspace=0)
fig_intc_fracture = plot.plt.figure(plot.id_intc_fracture+11, figsize=(16, 6))
fig_intc_fracture.subplots_adjust(hspace=0, wspace=0)
fig_outflux = plot.plt.figure(plot.id_outflux+11, figsize=(16, 6))
fig_outflux.subplots_adjust(hspace=0, wspace=0)

for title, refinement in zip(titles, refinement_index):

    axes_intc_matrix = fig_intc_matrix.add_subplot(1, 3, int(refinement) + 1, ylim=(0-10, 175+10))
    axes_intc_fracture = fig_intc_fracture.add_subplot(1, 3, int(refinement) + 1, ylim=(0, 0.45))
    axes_outflux = fig_outflux.add_subplot(1, 3, int(refinement) + 1, ylim=(0-0.00000005, 0.0000014+0.00000005))

    folder = "./cases/regular/results/" 
    data = os.path.join(folder, f"dot_cond{cond}_{refinement}.csv")

    plot.plot_over_time(data, label, refinement, plot.id_intc_matrix, title, axes_intc_matrix,
                        plot.linestyle[place][method], plot.color[place][method],
                        has_legend=False, ylim=(0-10, 175+10))
    plot.plot_over_time(data, label, refinement, plot.id_intc_fracture, title, axes_intc_fracture,
                        plot.linestyle[place][method], plot.color[place][method],
                        has_legend=False, ylim=(0, 0.45))
    plot.plot_over_time(data, label, refinement, plot.id_outflux, title, axes_outflux,
                        plot.linestyle[place][method], plot.color[place][method],
                        has_legend=False, ylim=(0-0.00000005, 0.0000014+0.00000005))
# save figures
plot.save(plot.id_intc_matrix, "case_single_pot_c_matrix")
plot.save(plot.id_intc_fracture, "case_single_pot_c_fracture")
plot.save(plot.id_outflux, "case_single_pot_outflux")

# ncol = 4
# for place in places_and_methods:
#     for method in places_and_methods[place]:
#         label = "\\texttt{" + place + "-" + method + "}"
#         plot.plot_legend(label, plot.id_intc_matrix_legend, plot.linestyle[place][method],
#                          plot.color[place][method], ncol)
#         plot.plot_legend(label, plot.id_intc_fracture_legend, plot.linestyle[place][method],
#                          plot.color[place][method], ncol)
#         plot.plot_legend(label, plot.id_outflux_legend, plot.linestyle[place][method],
#                          plot.color[place][method], ncol)

# plot.save(plot.id_intc_matrix_legend, "case_single_pot_c_matrix_legend")
# plot.crop_pdf("case_single_pot_c_matrix_legend")
# plot.save(plot.id_intc_fracture_legend, "case_single_pot_c_fracture_legend")
# plot.crop_pdf("case_single_pot_c_fracture_legend")
# plot.save(plot.id_outflux_legend, "case_single_pot_outflux_legend")
# plot.crop_pdf("case_single_pot_outflux_legend")

#------------------------------------------------------------------------------#
