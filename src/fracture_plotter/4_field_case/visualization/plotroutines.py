# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from operator import methodcaller

from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *

# ids of the different plots
id_p_0_matrix = 0  # pressure along (0, 100, 100)-(100, 0, 0)
id_p_0_matrix_legend = 10  # pressure along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix = 1  # p along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix_legend = 11  # p along (0, 100, 100)-(100, 0, 0)
id_pot = 2
id_pot_legend = 12  # p along (0, 100, 100)-(100, 0, 0)


def plot_over_line(
    filename, label, ID, title, ax, linestyle="-", color="C0", fontsize=30, **kwargs
):
    # Define the converter for the input data
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 2  # Assumes the number of columns is 2 for regular data

    # Check if the filename contains 'mean' to determine if we're plotting mean and std
    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(
            filename=filename,
            n_columns=N,
            converters=dict(zip(range(N), [c] * N)),
            skip_header=1,
        )

        # Plot standard deviation band (mean +/- std)
        ax.fill_between(
            mean_data[:, 0],
            mean_data[:, 1] - std_data[:, 1],
            mean_data[:, 1] + std_data[:, 1],
            color=color,
            alpha=0.3,
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
        # Plot only the mean data
        data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        ax.plot(data[:, 0], data[:, 1], label=label, linestyle=linestyle, color=color)

    # Format y-axis using scientific notation
    formatter = mticker.ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-2, 2))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set_visible(True)
    ax.yaxis.get_offset_text().set_fontsize(fontsize)

    # Set x-axis label and grid
    ax.set_xlabel(styles.getArcLengthLabel(), fontsize=fontsize)
    ax.set_ylabel(styles.getHeadLabel(3), fontsize=fontsize)
    ax.grid(True)

    # Set plot title if needed
    if kwargs.get("show_title", True):
        ax.set_title(title, fontsize=fontsize)

    # Set legend if needed
    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)

    # Set xlim and ylim if provided
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))

    # Set specific ticks depending on the ID
    if ID == id_p_0_matrix:
        ax.set_xticks([0, 500, 1000, 1500])
        ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700])
    elif ID == id_p_1_matrix:
        ax.set_xticks([0, 500, 1000, 1500])
        ax.set_yticks([0, 50, 100, 150, 200, 250])


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
    **kwargs,
):
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 53  # Number of columns in the file

    # Check if the filename contains 'mean' to determine if we're plotting mean and std
    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(
            filename=filename,
            n_columns=N,
            converters=dict(zip(range(N), [c] * N)),
            skip_header=1,
        )

        # Time and values for mean and std
        time = mean_data[:, 0]
        mean_values = mean_data[:, region + 1]
        std_values = std_data[:, region + 1]

        # Plot the mean with a shaded region for the standard deviation
        ax.fill_between(
            time,
            mean_values - std_values,
            mean_values + std_values,
            color=color,
            alpha=0.3,
        )
        ax.plot(time, mean_values, label=label, linestyle=linestyle, color=color)
    else:
        # Plot the regular data
        data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        time = data[:, 0]
        values = data[:, region + 1]
        ax.plot(time, values, label=label, linestyle=linestyle, color=color)

    # Format y-axis using scientific notation
    plt.rcParams.update({"figure.max_open_warning": 0})

    format_axis(ax, region_pos, fontsize)

    # Set x-axis label and grid
    ax.set_xlabel(styles.getTimeLabel("s"), fontsize=fontsize)
    ax.set_ylabel(styles.getAveragedConcentrationLabel(2), fontsize=fontsize)
    ax.grid(True)

    # Set plot title if needed
    if kwargs.get("show_title", True):
        ax.set_title(title, fontsize=fontsize)

    # Set legend if needed
    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)

    # Set xlim and ylim if provided
    if kwargs.get("xlim", None):
        plt.xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))

    # Set specific xticks
    ax.set_xticks([0, 500, 1000, 1500])


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1, fontsize=30):
    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol, fontsize=fontsize)


def plot_percentiles(ref, places_and_methods, ax, fontsize=30, **kwargs):
    paths = get_paths(__file__)

    c = lambda s: float(s.decode().replace("D", "e"))
    N = 2

    f = []
    minX = -np.inf
    maxX = np.inf

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method)
            datafile = os.path.join(folder, f"dol_line_{ref}.csv").replace("\_", "_")
            data = np.genfromtxt(
                datafile, delimiter=",", converters=dict(zip(range(N), [c] * N))
            )
            # only take the interesting columns and eleminate nan rows
            data = data[:, 0:2]
            data = data[~np.isnan(data).any(axis=1)]

            f.append(interpolate.interp1d(data[:, 0], data[:, 1]))
            minX = max(minX, data[0, 0])
            maxX = min(maxX, data[-1, 0])

    ls = np.linspace(minX, maxX, num=1000)
    interpolateddata = list(map(methodcaller("__call__", ls), f))
    meanvalues = np.mean(interpolateddata, axis=0)
    variance = np.var(interpolateddata, axis=0)
    lowerpercentile = np.percentile(interpolateddata, 10, axis=0)
    upperpercentile = np.percentile(interpolateddata, 90, axis=0)

    ax.fill_between(ls, lowerpercentile, upperpercentile, color="gray")
    ax.grid(True)
    ax.set_xlabel(styles.getArcLengthLabel(), fontsize=fontsize)
    weightedarea = (simps(upperpercentile, ls) - simps(lowerpercentile, ls)) / simps(
        meanvalues, ls
    )
    title = "weighted area " + MathTextSciFormatter("%1.2e")(weightedarea)
    ax.title.set_text(title)
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))

    ax.set_xticks([0, 500, 1000, 1500])
    if ref == "0":
        ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700])
    elif ref == "1":
        ax.set_yticks([0, 50, 100, 150, 200, 250])

    # choose y-label depending on plot id
    ax.set_ylabel(styles.getHeadLabel(3), fontsize=fontsize)

    return (ls, lowerpercentile, upperpercentile)
