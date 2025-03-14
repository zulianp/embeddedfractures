# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *

# ids of the different plots
id_p_0_matrix = 0  # pressure along (0, 100, 100)-(100, 0, 0)
id_p_0_matrix_legend = 10  # pressure along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix = 1  # p along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix_legend = 11  # p along (0, 100, 100)-(100, 0, 0)
id_pot_legend = 12  # p along (0, 100, 100)-(100, 0, 0)


def plot_legend_in_middle(fig, ax1, ax2):
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
        fontsize=14,
    )


def plot_over_line(
    file_name,
    label,
    simulation_id,
    title,
    cond,
    ax,
    linestyle="-",
    color="C0",
    **kwargs,
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

    # Set optional title and legend
    if kwargs.get("has_title", True):
        ax.set_title(title)

    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Apply optional x and y limits
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


def plot_over_time(
    file_name, legend, ref, ID, title, ax, linestyle="-", color="C0", **kwargs
):
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 9  # Assuming 9 columns of data

    if "mean" in file_name:
        std_filename = file_name.replace("mean", "std")
        mean_data = np.genfromtxt(
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
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
        ax.plot(time, mean_values, label=legend, linestyle=linestyle, color=color)
    else:
        data = np.genfromtxt(
            file_name, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        ax.plot(
            data[:, 0], data[:, ID + 1], label=legend, linestyle=linestyle, color=color
        )

    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    ax.set_xlabel(styles.getTimeLabel("s"))  # Only apply xlabel

    # Apply ylabel only to the first subplot
    ax.set_ylabel(r"$\overline{c_2}$")
    ax.grid(True)

    if kwargs.get("has_title", True):
        title_fig = title + " - fracture " + str(ID)
        ax.set_title(title_fig)

    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

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


def save_over_time(filename, extension=".pdf", plots_dir=None):
    for ID in np.arange(8):
        save(
            ID,
            filename + "_fracture_" + str(ID),
            extension=extension,
            plots_dir=plots_dir,
        )


def plot_boundary_data(
    fig, axs, data, methods, data_ref, colors, linestyle, extension=".pdf"
):
    """
    Plots the boundary data on provided axes.

    Parameters:
      fig   : matplotlib Figure object.
      axs   : dict with axes for each subplot, e.g.,
              {"head": ax_head, "flux": ax_flux, "ref_flux": ax_ref_flux}
      data  : Data array.
      methods, colors, linestyle : Plot styling parameters.
      data_ref : Reference data array.
    """
    plot_boundary_head(
        ax=axs["head"],
        da=data[:, 4:],
        methods=methods,
        head_ref=data_ref[2],
        colors=colors,
        linestyle=linestyle,
    )
    plot_boundary_fluxes(
        ax=axs["flux"],
        da=data[:, :4],
        methods=methods,
        ratio_ref=data_ref[1],
        colors=colors,
        linestyle=linestyle,
    )
    plot_reference_fluxes(
        ax=axs["ref_flux"],
        da=data[:, :4],
        methods=methods,
        ratio_ref=data_ref[1],
        colors=colors,
        linestyle=linestyle,
    )


def plot_boundary_fluxes(ax, da, methods, ratio_ref, colors, linestyle):
    N = da.shape[0]
    ind = np.arange(N)
    width = 0.2
    x = np.array([0, N])
    ax.plot(x, np.array([ratio_ref, ratio_ref]), ls="-", color="black")

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
    ax.set_xticklabels(["\\textbf{" + str(idx) + "}" for idx in ind])
    ax.text(
        0.5,
        -0.2,
        "\\textbf{subfig. b}",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )


def plot_reference_fluxes(ax, da, methods, ratio_ref, colors, linestyle):
    N = da.shape[0]
    ind = np.arange(N)
    width = 0.2
    x = np.array([0, N])
    ax.plot(x, np.array([1 / 3, 1 / 3]), ls="-", color="black")

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
    ax.set_xticklabels(["\\textbf{" + str(idx) + "}" for idx in ind])
    ax.text(
        0.5,
        -0.2,
        "\\textbf{subfig. a}",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )


def plot_boundary_head(ax, da, methods, head_ref, colors, linestyle):
    N = da.shape[0]
    ind = np.arange(N)
    width = 0.3
    x = np.array([0, N])
    ax.plot(x, np.array([head_ref, head_ref]), ls="-", color="black")

    colors = [colors, colors]
    for i, c in enumerate(colors):
        ax.bar(ind + width * i, da[:, i], width, color=c, edgecolor="white")

    linestyle = [item for sublist in [linestyle, linestyle] for item in sublist]
    linestyle_map = {"-": "", "--": "-", ":": "--"}
    linestyle = [linestyle_map[item] for item in linestyle]
    for bar, hatch in zip(ax.patches, linestyle):
        bar.set_hatch(hatch)

    ax.legend(["Reference " + styles.getHeadLabel(3)])
    ax.set_ylabel(styles.getHeadLabel(3))
    ax.set_ylim([0.16, 0.28])
    ax.set_xticks(ind + width)
    ax.set_xticklabels(["\\textbf{" + str(idx) + "}" for idx in ind])
    ax.text(
        0.5,
        -0.2,
        "\\textbf{subfig. c}",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )


def plot_percentiles(ref, line_id, places_and_methods, ax, **kwargs):

    c = lambda s: float(s.decode().replace("D", "e"))
    N = 2

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

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
