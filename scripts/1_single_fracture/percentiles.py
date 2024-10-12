import os
import plotroutines as plot

def setup_figure(id_offset, num_axes, ylim):
    fig = plot.plt.figure(id_offset + 11, figsize=(16, 8))  # Increased figure height for layout consistency
    fig.subplots_adjust(hspace=0.4, wspace=0)  # Adjust space between plots vertically
    axes_list = [fig.add_subplot(1, num_axes, idx + 1, ylim=ylim) for idx in range(num_axes)]
    return fig, axes_list

def plot_percentiles(ref, plot_id, places_and_methods, ax):
    plot.plot_percentiles(ref, plot_id, places_and_methods, ax)

def run_percentiles():
    curr_dir = os.path.dirname(os.path.realpath(__file__))  # current directory
    case = curr_dir.split(os.sep)[-1]  # case we are dealing with

    places_and_methods = {
        "USI": ["FEM\_LM"],
        "mean": ["key"],
    }

    # Setup figures and axes
    fig_p_matrix, axes_p_matrix_list = setup_figure(plot.id_p_matrix, 3, ylim=(1-0.1, 4+0.1))
    fig_c_matrix, axes_c_matrix_list = setup_figure(plot.id_c_matrix, 3, ylim=(0-0.0005, 0.01+0.0005))
    fig_c_fracture, axes_c_fracture_list = setup_figure(plot.id_c_fracture, 3, ylim=(0.0075, 0.0101))

    # Plot percentiles for each refinement level
    for ref, idx, axes_p_matrix, axes_c_matrix, axes_c_fracture in zip(["0", "1", "2"], range(3), axes_p_matrix_list, axes_c_matrix_list, axes_c_fracture_list):
        plot_percentiles(ref, plot.id_p_matrix, places_and_methods, axes_p_matrix)
        plot_percentiles(ref, plot.id_c_matrix, places_and_methods, axes_c_matrix)
        plot_percentiles(ref, plot.id_c_fracture, places_and_methods, axes_c_fracture)

    # Save figures
    plot.save(plot.id_p_matrix, f"{case}_pol_p_matrix_percentile_90_10", starting_from=3)
    plot.save(plot.id_c_matrix, f"{case}_pol_c_matrix_percentile_90_10", starting_from=3)
    plot.save(plot.id_c_fracture, f"{case}_pol_c_fracture_percentile_90_10", starting_from=3)


if __name__ == "__main__":
    run_percentiles()
