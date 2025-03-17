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
id_pot_legend = 12  # p along (0, 100, 100)-(100, 0, 0)


def plot_legend_in_middle(fig, ax1, ax2, fontsize=30):
    # Combine handles and labels from both axes
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    # Create a unique set of handles and labels (in case both axes share labels)
    handles = handles1 + handles2
    labels = labels1 + labels2

    # Remove duplicates from the legend
    unique_handles, unique_labels = [], []
    for handle, label in zip(handles, labels):
        if label not in unique_labels:
            unique_handles.append(handle)
            unique_labels.append(label)

    # Plot the combined legend centered below the subplots
    fig.legend(
        unique_handles,
        unique_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=4,
        fontsize=fontsize,
    )


def plot_over_line(
    filename,
    label,
    ref,
    title,
    ax,
    linestyle="-",
    color="C0",
    fontsize=30,
    **kwargs,
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

    # Set optional title and legend
    if kwargs.get("show_title", True):
        ax.set_title(title, fontsize=fontsize)

    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)

    # Apply optional x and y limits
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


def plot_over_time(
    filename,
    label,
    ref,
    ID,
    title,
    ax,
    linestyle="-",
    color="C0",
    fontsize=30,
    **kwargs,
):
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 9  # Assuming 9 columns of data

    if "mean" in filename:
        std_filename = filename.replace("mean", "std")
        mean_data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        std_data = np.genfromtxt(
            std_filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )

        if mean_data.shape != std_data.shape:
            raise ValueError(
                "Mean and standard deviation data do not have the same shape!"
            )

        time = mean_data[:, 0]
        mean_values = mean_data[:, ID + 1]
        std_values = std_data[:, ID + 1]

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
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        ax.plot(
            data[:, 0], data[:, ID + 1], label=label, linestyle=linestyle, color=color
        )

    format_axis(ax, ref, fontsize)

    ax.set_xlabel(styles.getTimeLabel("s"), fontsize=fontsize)  # Only apply xlabel

    # Apply ylabel only to the first subplot
    ax.set_ylabel(r"$\overline{c_2}$")
    ax.grid(True)

    if kwargs.get("show_title", True):
        title_fig = title + " - fracture " + str(ID)
        ax.set_title(title_fig, fontsize=fontsize)

    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)

    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1, fontsize=30):
    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol, fontsize=fontsize)


def save_over_time(filename, extension=".pdf", plots_dir=None, fontsize=25):
    for ID in np.arange(8):
        save(
            ID=ID,
            filename=filename + "_fracture_" + str(ID),
            extension=extension,
            plots_dir=plots_dir,
            fontsize=fontsize,
        )


def plot_boundary_data(data, methods, data_ref, colors, linestyle, extension=".pdf"):
    plot_boundary_head(data[:, 4:], methods, data_ref[2], colors, linestyle, extension)
    plot_boundary_fluxes(
        data[:, :4], methods, data_ref[1], colors, linestyle, extension
    )
    plot_reference_fluxes(
        data[:, :4], methods, data_ref[1], colors, linestyle, extension
    )


def plot_boundary_fluxes(da, methods, ratio_ref, colors, linestyle, extension):
    paths = get_paths(__file__)

    N = da.shape[0]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = np.array([0, N])

    c1 = "black"
    ax.plot(x, np.array([ratio_ref, ratio_ref]), ls="-", color=c1)
    colors = [colors, colors]
    for i, c in enumerate(colors):
        ax.bar(ind + width * i, da[:, i + 2], width, color=c, edgecolor="white")

    linestyle = [item for sublist in [linestyle, linestyle] for item in sublist]
    linestyle_map = {"-": "", "--": "-", ":": "--"}
    linestyle = [linestyle_map[item] for item in linestyle]
    for bar, hatch in zip(ax.patches, linestyle):
        bar.set_hatch(hatch)

    ax.legend(["Reference flux ratio $r_{out}$"])
    ax.set_ylabel("$r_{out}$")

    ax.set_ylim([0.4, 0.5])
    ax.set_xticks(ind + width)
    ind_str = ["\\textbf{" + str(idx) + "}" for idx in ind]
    ax.set_xticklabels(ind_str)
    os.makedirs(paths.plots_dir, exist_ok=True)

    text = "\\textbf{subfig. b}"
    ax.text(
        0.5,
        -0.2,
        text,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )

    plt.savefig(
        os.path.join(paths.plots_dir, f"{paths.case}_boundary_head" + extension),
        bbox_inches="tight",
    )


def plot_reference_fluxes(da, colors, linestyle, extension):
    paths = get_paths(__file__)

    N = da.shape[0]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = np.array([0, N])
    c0 = "black"
    ax.plot(x, np.array([1 / 3, 1 / 3]), ls="-", color=c0)
    colors = [colors, colors]
    for i, c in enumerate(colors):
        ax.bar(ind + width * i, da[:, i], width, color=c, edgecolor="white")

    linestyle = [item for sublist in [linestyle, linestyle] for item in sublist]
    linestyle_map = {"-": "", "--": "-", ":": "--"}
    linestyle = [linestyle_map[item] for item in linestyle]
    for bar, hatch in zip(ax.patches, linestyle):
        bar.set_hatch(hatch)

    ax.legend(["Prescribed flux $\\overline{u}_{out}$"])
    ax.set_ylabel("$\\overline{u}_{out}$")

    ax.set_ylim([0.1, 0.42])
    ax.set_xticks(ind + width)
    ind_str = ["\\textbf{" + str(idx) + "}" for idx in ind]
    ax.set_xticklabels(ind_str)
    os.makedirs(paths.plots_dir, exist_ok=True)

    text = "\\textbf{subfig. a}"
    ax.text(
        0.5,
        -0.2,
        text,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )

    plt.savefig(
        os.path.join(paths.plots_dir, f"{paths.case}_reference_flux" + extension),
        bbox_inches="tight",
    )


def plot_boundary_head(da, methods, head_ref, colors, linestyle, extension):
    paths = get_paths(__file__)

    N = da.shape[0]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.3  # the width of the bars
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.array([0, N])
    c0 = "black"
    ax.plot(x, np.array([head_ref, head_ref]), ls="-", color=c0)
    colors = [colors, colors]

    for i, c in enumerate(colors):
        ax.bar(
            ind + width * i, da[:, i], width, color=c, edgecolor="white"
        )  # , hatch=linestyle)

    linestyle = [item for sublist in [linestyle, linestyle] for item in sublist]
    linestyle_map = {"-": "", "--": "-", ":": "--"}
    linestyle = [linestyle_map[item] for item in linestyle]
    for bar, hatch in zip(ax.patches, linestyle):
        bar.set_hatch(hatch)

    ax.legend(["Reference " + styles.getHeadLabel(3)])
    ax.set_ylabel(styles.getHeadLabel(3))
    ax.set_ylim([0.16, 0.28])
    ax.set_xticks(ind + width)
    ind_str = ["\\textbf{" + str(idx) + "}" for idx in ind]
    ax.set_xticklabels(ind_str)

    os.makedirs(paths.plots_dir, exist_ok=True)

    text = "\\textbf{subfig. c}"
    ax.text(
        0.5,
        -0.2,
        text,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )

    plt.savefig(
        os.path.join(paths.plots_dir, f"{paths.case}_boundary_fluxes" + extension),
        bbox_inches="tight",
    )


def plot_percentiles(ref, line_id, places_and_methods, ax, **kwargs):

    c = lambda s: float(s.decode().replace("D", "e"))
    N = 2

    f = []
    minX = -np.inf
    maxX = np.inf

    for place in places_and_methods:
        for method in places_and_methods[place]:
            base_dir = os.getcwd().replace("scripts", "results")
            folder = os.path.join(base_dir, place, method)
            datafile = os.path.join(
                folder, "dol_line_" + line_id + "_refinement_" + ref + ".csv"
            ).replace("\_", "_")
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
