# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from operator import methodcaller

from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *


def plot_legend_in_middle(ax, fontsize=14):
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=4,
        fontsize=fontsize,
    )  # Legend below the plot


def plot_over_line(
    filename, label, ref, title, ax, linestyle="-", color="C0", fontsize=30, **kwargs
):
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 2  # Assuming two columns of data (x, y)

    # Check if the filename contains 'mean' to determine if we're plotting mean and std
    if "mean" in filename:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = filename.replace("mean", "std")

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        std_data = np.genfromtxt(
            std_filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )

        # Ensure that the mean and std arrays have consistent shapes
        if mean_data.shape != std_data.shape:
            raise ValueError(
                "Mean and standard deviation data do not have the same shape!"
            )

        # Plot standard deviation band (mean +/- std)
        ax.fill_between(
            mean_data[:, 0],
            mean_data[:, 1] - std_data[:, 1],
            mean_data[:, 1] + std_data[:, 1],
            color=color,
            alpha=0.5,
        )  # Adjust transparency for visibility

        # Plot the mean data line
        ax.plot(
            mean_data[:, 0],
            mean_data[:, 1],
            label=label,
            linestyle=linestyle,
            color=color,
        )

    else:
        # Plot only the mean data if 'mean' is not in the file name
        data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        ax.plot(data[:, 0], data[:, 1], label=label, linestyle=linestyle, color=color)

    format_axis(ax, ref, fontsize)

    # Set labels, grid, and title
    ax.set_xlabel(styles.getArcLengthLabel(), fontsize=fontsize)
    ax.set_ylabel(styles.getHeadLabel(3), fontsize=fontsize)
    ax.grid(True)

    if kwargs.get("show_title", True):
        ax.set_title(title, fontsize=fontsize)

    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)

    # Apply x and y limits if provided
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


def plot_over_time(
    filename,
    label,
    title,
    region,
    region_pos,
    ax,
    linestyle="-",
    color="C0",
    fontsize=30,
    **kwargs
):
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 22

    # Determine if the file contains 'mean' to plot mean and std
    if "mean" in filename:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = filename.replace("mean", "std")

        # Get the number of columns
        N_temp = len(np.genfromtxt(filename, delimiter=",", max_rows=1, skip_header=1))
        if N_temp < N:
            N = N_temp

        # Read the mean and standard deviation data
        mean_data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        std_data = np.genfromtxt(
            std_filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )

        plt.rcParams.update({"figure.max_open_warning": 0})
        format_axis(ax, region_pos, fontsize)

        # Plot the mean with a shaded region for the standard deviation
        time = mean_data[:, 0]
        mean_values = mean_data[:, region + 1]
        std_values = std_data[:, region + 1]

        ax.fill_between(
            time,
            mean_values - std_values,
            mean_values + std_values,
            color=color,
            alpha=0.3,
        )
        ax.plot(time, mean_values, label=label, linestyle=linestyle, color=color)

    else:
        # Plot only the mean data if 'mean' is not in the file name
        N_temp = len(np.genfromtxt(filename, delimiter=",", max_rows=1, skip_header=1))
        if N_temp < N:
            N = N_temp

        data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )

        plt.rcParams.update({"figure.max_open_warning": 0})

        format_axis(ax, region_pos, fontsize)

        region_idx = region + 1
        if "/USI/" in filename:
            if region == 1:
                region_idx = 1
            elif region == 10:
                region_idx = 2
            elif region == 11:
                region_idx = 3

        # Plot the mean data
        ax.plot(
            data[:, 0],
            data[:, region_idx],
            label=label,
            linestyle=linestyle,
            color=color,
        )

    # Set labels and grid
    ax.set_xlabel(styles.getTimeLabel(), fontsize=fontsize)
    ax.set_ylabel(styles.getConcentrationLabel(3), fontsize=fontsize)
    ax.grid(True)

    # Set title and legend if required
    if kwargs.get("show_title", True):
        ax.set_title(title, fontsize=fontsize)
    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)

    # Apply x and y limits if provided
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1, fontsize=30):
    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol, fontsize=fontsize)


# def plot_percentiles(ref, cond, places_and_methods, ax, fontsize=30, **kwargs):
#     paths = get_paths(__file__)

#     c = lambda s: float(s.decode().replace("D", "e"))
#     N = 2

#     f = []
#     minX = -np.inf
#     maxX = np.inf

#     for place in places_and_methods:
#         for method in places_and_methods[place]:
#             folder = os.path.join(paths.results_dir, place, method)
#             datafile = (
#                 folder.replace("\\", "")
#                 + "dol_cond_"
#                 + cond
#                 + "_refinement_"
#                 + ref
#                 + ".csv"
#             )
#             data = np.genfromtxt(
#                 datafile, delimiter=",", converters=dict(zip(range(N), [c] * N))
#             )
#             data = data[:, 0:2]
#             data = data[~np.isnan(data).any(axis=1)]

#             f.append(interpolate.interp1d(data[:, 0], data[:, 1]))
#             minX = max(minX, data[0, 0])
#             maxX = min(maxX, data[-1, 0])

#     ls = np.linspace(minX, maxX, num=1000)
#     interpolateddata = list(map(methodcaller("__call__", ls), f))
#     meanvalues = np.mean(interpolateddata, axis=0)
#     variance = np.var(interpolateddata, axis=0)
#     upperpercentile = np.percentile(interpolateddata, 90, axis=0)
#     lowerpercentile = np.percentile(interpolateddata, 10, axis=0)

#     ax.fill_between(ls, lowerpercentile, upperpercentile, color="gray")
#     ax.grid(True)
#     ax.set_xlabel(styles.getArcLengthLabel(), fontsize=fontsize)
#     weightedarea = (simps(upperpercentile, ls) - simps(lowerpercentile, ls)) / simps(
#         meanvalues, ls
#     )
#     title = "weighted area " + MathTextSciFormatter("%1.2e")(weightedarea)
#     ax.title.set_text(title)
#     if kwargs.get("ylim", None):
#         plt.ylim(kwargs.get("ylim"))

#     ax.set_ylabel(styles.getHeadLabel(3), fontsize=fontsize)

#     return (ls, lowerpercentile, upperpercentile)
