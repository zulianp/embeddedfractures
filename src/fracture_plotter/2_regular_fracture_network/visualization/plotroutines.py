# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from fracture_plotter.utils.plot_routines_utils import *


def plot_legend_in_middle(ax):
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=4,
        fontsize=14,
    )  # Legend below the plot


def plot_over_line(
    file_name,
    label,
    simulation_id,
    title,
    cond,
    ax,
    linestyle="-",
    color="C0",
    **kwargs
):
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 2  # Assuming two columns of data (x, y)

    # Check if the file_name contains 'mean' to determine if we're plotting mean and std
    if "mean" in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace("mean", "std")

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
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
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        ax.plot(data[:, 0], data[:, 1], label=label, linestyle=linestyle, color=color)

    # Format the y-axis
    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

    # Modify tick parameters for simulations other than the first
    if simulation_id > 0:
        ax.yaxis.set_tick_params(length=0)

    # Set labels, grid, and title
    ax.set_xlabel(styles.getArcLengthLabel())
    ax.set_ylabel(styles.getHeadLabel(3))
    ax.grid(True)

    if kwargs.get("has_title", True):
        ax.set_title(title)

    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Apply x and y limits if provided
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


def crop_pdf(filename):
    paths = get_paths(__file__)

    filename = os.path.join(paths.plots_dir, filename + ".pdf")
    if os.path.isfile(filename):
        os.system("pdfcrop --margins '0 -400 0 0' " + filename + " " + filename)
        os.system("pdfcrop " + filename + " " + filename)


def plot_over_time(
    file_name,
    legend,
    title,
    cond,
    region,
    region_pos,
    num_regions,
    ax,
    linestyle="-",
    color="C0",
    **kwargs
):
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 22

    # Determine if the file contains 'mean' to plot mean and std
    if "mean" in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace("mean", "std")

        # Get the number of columns
        N_temp = len(np.genfromtxt(file_name, delimiter=",", max_rows=1, skip_header=1))
        if N_temp < N:
            N = N_temp

        # Read the mean and standard deviation data
        mean_data = np.genfromtxt(
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        std_data = np.genfromtxt(
            std_filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )

        # Format the y-axis
        ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

        plt.rcParams.update({"figure.max_open_warning": 0})

        # Modify tick parameters if needed
        if region_pos > 0:
            ax.yaxis.set_tick_params(length=0)

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
        ax.plot(time, mean_values, label=legend, linestyle=linestyle, color=color)

    else:
        # Plot only the mean data if 'mean' is not in the file name
        N_temp = len(np.genfromtxt(file_name, delimiter=",", max_rows=1, skip_header=1))
        if N_temp < N:
            N = N_temp

        data = np.genfromtxt(
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )

        ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

        plt.rcParams.update({"figure.max_open_warning": 0})

        # Modify tick parameters if needed
        if region_pos > 0:
            ax.yaxis.set_tick_params(length=0)

        region_idx = region + 1
        if "/USI/" in file_name:
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
            label=legend,
            linestyle=linestyle,
            color=color,
        )

    # Set labels and grid
    ax.set_xlabel(styles.getTimeLabel())
    ax.set_ylabel(styles.getConcentrationLabel(3))
    ax.grid(True)

    # Set title and legend if required
    if kwargs.get("has_title", True):
        ax.set_title(title)
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Apply x and y limits if provided
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1):
    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol)


class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2e"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        if "f" in self.fmt:
            return "${}$".format(s)
        decimal_point = "."
        positive_sign = "+"
        tup = s.split("e")
        significand = tup[0].rstrip(decimal_point)
        sign = tup[1][0].replace(positive_sign, "")
        exponent = tup[1][1:].lstrip("0")
        if exponent:
            exponent = "10^{%s%s}" % (sign, exponent)
        if significand and exponent:
            s = r"%s{\times}%s" % (significand, exponent)
        else:
            s = r"%s%s" % (significand, exponent)
        return "${}$".format(s)


def plot_percentiles(ref, cond, places_and_methods, ax, **kwargs):
    paths = get_paths(__file__)

    c = lambda s: float(s.decode().replace("D", "e"))
    N = 2

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    f = []
    minX = -np.inf
    maxX = np.inf

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method)
            datafile = (
                folder.replace("\\", "")
                + "dol_cond_"
                + cond
                + "_refinement_"
                + ref
                + ".csv"
            )
            data = np.genfromtxt(
                datafile, delimiter=",", converters=dict(zip(range(N), [c] * N))
            )
            data = data[:, 0:2]
            data = data[~np.isnan(data).any(axis=1)]

            f.append(interpolate.interp1d(data[:, 0], data[:, 1]))
            minX = max(minX, data[0, 0])
            maxX = min(maxX, data[-1, 0])

    ls = np.linspace(minX, maxX, num=1000)
    interpolateddata = list(map(methodcaller("__call__", ls), f))
    meanvalues = np.mean(interpolateddata, axis=0)
    variance = np.var(interpolateddata, axis=0)
    upperpercentile = np.percentile(interpolateddata, 90, axis=0)
    lowerpercentile = np.percentile(interpolateddata, 10, axis=0)

    ax.fill_between(ls, lowerpercentile, upperpercentile, color="gray")
    ax.grid(True)
    ax.set_xlabel(styles.getArcLengthLabel())
    weightedarea = (simps(upperpercentile, ls) - simps(lowerpercentile, ls)) / simps(
        meanvalues, ls
    )
    title = "weighted area " + MathTextSciFormatter("%1.2e")(weightedarea)
    ax.title.set_text(title)
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))

    ax.set_ylabel(styles.getHeadLabel(3))

    return (ls, lowerpercentile, upperpercentile)
