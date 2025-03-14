# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import sys
from operator import methodcaller

from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *

# ids of the different plots
id_p_matrix = 0  # pressure along (0, 100, 100)-(100, 0, 0)
id_p_matrix_legend = 10  # pressure along (0, 100, 100)-(100, 0, 0)
id_c_matrix = 1  # c along (0, 100, 100)-(100, 0, 0)
id_c_matrix_legend = 11  # c along (0, 100, 100)-(100, 0, 0)
id_c_fracture = 2  # c along (0, 100, 80)-(100, 0, 20)
id_c_fracture_legend = 12  # c along (0, 100, 80)-(100, 0, 20)


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
    file_name, label, ref, ID, title, ax, linestyle="-", color="C0", **kwargs
):
    # Define the converter for the input data
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 5  # Assumes the number of columns is 5

    # Check if the file_name contains 'mean' to determine if we're plotting mean and std
    if "mean" in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace("mean", "std")

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(
            file_name,
            delimiter=",",
            skip_header=1,
            converters=dict(zip(range(N), [c] * N)),
        )
        std_data = np.genfromtxt(
            std_filename,
            delimiter=",",
            skip_header=1,
            converters=dict(zip(range(N), [c] * N)),
        )

        # Ensure that the mean and std arrays have consistent shapes
        if mean_data.shape != std_data.shape:
            raise ValueError(
                "Mean and standard deviation data do not have the same shape!"
            )

        # Plot standard deviation band (mean +/- std)
        ax.fill_between(
            mean_data[:, 2 * ID],
            mean_data[:, 2 * ID + 1] - std_data[:, 2 * ID + 1],
            mean_data[:, 2 * ID + 1] + std_data[:, 2 * ID + 1],
            color=color,
            alpha=0.5,
        )  # Adjust transparency for visibility

        # Plot the mean data line
        ax.plot(
            mean_data[:, 2 * ID],
            mean_data[:, 2 * ID + 1],
            label=label,
            linestyle=linestyle,
            color=color,
        )
    else:
        # Plot only the mean data
        data = np.genfromtxt(
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        ax.plot(
            data[:, 2 * ID],
            data[:, 2 * ID + 1],
            label=label,
            linestyle=linestyle,
            color=color,
        )

    # Format y-axis using scientific notation
    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    # Remove y-axis ticks if ref is set
    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    # Set x-axis label and grid
    ax.set_xlabel(styles.getArcLengthLabel())
    ax.grid(True)

    # Set plot title if needed
    if kwargs.get("has_title", True):
        ax.set_title(title)

    # Set legend if needed
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Choose y-label depending on plot id
    if ID == id_p_matrix:
        ax.set_ylabel(styles.getHeadLabel(3))
    elif ID == id_c_matrix:
        ax.set_ylabel(styles.getConcentrationLabel(3))
    elif ID == id_c_fracture:
        ax.set_ylabel(styles.getConcentrationLabel(2))
    else:
        print("Error: Invalid plot id provided.")
        sys.exit(1)


# ids of the different plots
id_intc_matrix = 0  # integral of c*porosity in the lower matrix sub-domain
id_intc_matrix_legend = 10  # integral of c*porosity in the lower matrix sub-domain
id_intc_fracture = 1  # indegral of c*porosity in the fracture
id_intc_fracture_legend = 11  # indegral of c*porosity in the fracture
id_outflux = 2  # integrated outflux across the outflow boundary
id_outflux_legend = 12  # integrated outflux across the outflow boundary


def plot_over_time(
    file_name, label, ref, ID, title, ax, linestyle="-", color="C0", **kwargs
):
    # Define the converter for the input data
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 4  # Assumes the number of columns is 4

    # Check if the file_name contains 'mean' to determine if we're plotting mean and std
    if "mean" in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace("mean", "std")

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(
            file_name,
            delimiter=",",
            skip_header=1,
            converters=dict(zip(range(N), [c] * N)),
        )
        std_data = np.genfromtxt(
            std_filename,
            delimiter=",",
            skip_header=1,
            converters=dict(zip(range(N), [c] * N)),
        )

        # Ensure that the mean and std arrays have consistent shapes
        if mean_data.shape != std_data.shape:
            raise ValueError(
                "Mean and standard deviation data do not have the same shape!"
            )

        time = mean_data[:, 0] / (365 * 24 * 3600)  # Convert time to years
        mean_values = mean_data[:, ID + 1]
        std_values = std_data[:, ID + 1]

        if ID == 1:
            print(f"mean file_name: {file_name}, std file_name: {std_filename}")
            print(
                f"Min(mean_values)={np.min(mean_values)}, Max(mean_values)={np.max(mean_values)}"
            )
            print(
                f"Min(std_values)={np.min(std_values)}, Max(std_values)={np.max(std_values)}"
            )

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
        data = np.genfromtxt(
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        time = data[:, 0] / (365 * 24 * 3600)  # Convert time to years
        ax.plot(time, data[:, ID + 1], label=label, linestyle=linestyle, color=color)

    # Format y-axis using scientific notation
    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    # Remove y-axis ticks if ref is set
    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    # Set x-axis label and grid
    ax.set_xlabel(styles.getTimeLabel("y"))
    ax.grid(True)

    # Set plot title if needed
    if kwargs.get("has_title", True):
        ax.set_title(title)

    # Set legend if needed
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Set x and y limits if provided
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))

    # Choose y-label depending on plot id
    if ID == id_intc_matrix:
        ax.set_ylabel("$\int_{\Omega_3} \phi_3 \, c_3$")
    elif ID == id_intc_fracture:
        ax.set_ylabel("$\int_{\Omega_2} \phi_2 \, c_2$")
    elif ID == id_outflux:
        ax.set_ylabel("outflux")
    else:
        print("Error: Invalid plot id provided.")
        sys.exit(1)


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1):
    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol)


class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2f"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        return "${}$".format(s)


def plot_percentiles(ref, ID, places_and_methods, ax, **kwargs):
    paths = get_paths(__file__)
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 6

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    f = []
    minX = -np.inf
    maxX = np.inf

    for place in places_and_methods:
        if place == "DTU" and ID != id_p_matrix:
            continue

        for method in places_and_methods[place]:
            folder = os.path.join(paths.results_dir, place, method)
            datafile = os.path.join(folder, f"dol_refinement_{ref}.csv").replace(
                "\_", "_"
            )
            data = np.genfromtxt(
                datafile, delimiter=",", converters=dict(zip(range(N), [c] * N))
            )
            # only take the interesting columns and eleminate nan rows
            data = data[:, 2 * ID : 2 * ID + 2]
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

    # choose y-label depending on plot id
    if ID == id_p_matrix:
        ax.set_ylabel(styles.getHeadLabel(3))
    elif ID == id_c_matrix:
        ax.set_ylabel(styles.getConcentrationLabel(3))
    elif ID == id_c_fracture:
        ax.set_ylabel(styles.getConcentrationLabel(2))
    else:
        print("Error. Invalid plot id provided.")
        sys.exit(1)

    return (ls, lowerpercentile, upperpercentile)
