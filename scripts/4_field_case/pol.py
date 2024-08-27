import os
import plotroutines as plot

#------------------------------------------------------------------------------#

# add data to plots

# add plots for the different schemes
# The first argument is the path to your data, where the data is assumed to be ordered comma-separated in the following order:
#   -> 1. arc length, 2. value of either c or pressure
# The second argument defines the legend you want to add to your data (Institution / Numerical method)

titles = ['a', 'b', 'c']
refinement_index = ['0', '1', '2']
cond = 1

fig_p_0 = plot.plt.figure(plot.id_p_0_matrix+11)
fig_p_1 = plot.plt.figure(plot.id_p_1_matrix+11)
ax_p_0 = fig_p_0.add_subplot(ylim=(-50, 720), xlim=(-100, 1800))
ax_p_1 = fig_p_1.add_subplot(ylim=(-20, 280), xlim=(-100, 1800))

label = "USI"
place = "ETHZ\_USI"
method = "FEM\_LM"

for title, ref in zip(titles, refinement_index):
        folder = "./cases/field/results/"
        # data = os.path.join(folder, f"dol_cond{cond}_{ref}.csv")

        title = "line 2"
        data = os.path.join(folder, f"dol_line2_refinement{ref}.csv")
        plot.plot_over_line(data, label,
                            plot.id_p_0_matrix, title, ax_p_0,
                            plot.linestyle[place][method], plot.color[place][method],
                            has_legend=False)
        title = "line 1"
        data = os.path.join(folder, f"dol_line1_refinement{ref}.csv")
        plot.plot_over_line(data, label,
                            plot.id_p_1_matrix, title, ax_p_1,
                            plot.linestyle[place][method], plot.color[place][method],
                            has_legend=False)

# save figures
ax_title = "\\textbf{subfig. b}"
plot.save(plot.id_p_0_matrix, "case_field_pol_line_2", ax_title=ax_title)
ax_title = "\\textbf{subfig. a}"
plot.save(plot.id_p_1_matrix, "case_field_pol_line_1", ax_title=ax_title)

# ncol = 4
# for place in places_and_methods:
#     for method in places_and_methods[place]:
#         label = "\\texttt{" + place + "-" + method + "}"
#         plot.plot_legend(label, plot.id_p_0_matrix_legend, plot.linestyle[place][method],
#                          plot.color[place][method], ncol)

#         plot.plot_legend(label, plot.id_p_1_matrix_legend, plot.linestyle[place][method],
#                              plot.color[place][method], ncol)

# plot.save(plot.id_p_0_matrix_legend, "case_field_pol_p_0_matrix_legend")
# plot.crop_pdf("case_field_pol_p_0_matrix_legend")
# plot.save(plot.id_p_1_matrix_legend, "case_field_pol_p_1_matrix_legend")
# plot.crop_pdf("case_field_pol_p_1_matrix_legend")


#------------------------------------------------------------------------------#
