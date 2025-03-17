# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from operator import methodcaller

from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *

# Plot IDs
id_p_0_matrix, id_p_0_matrix_legend = 0, 10
id_p_1_matrix, id_p_1_matrix_legend = 1, 11  # p along (0, 100, 100)-(100, 0, 0)
id_pot_legend = 12  # p along (0, 100, 100)-(100, 0, 0)


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
    N = 2
    load_args = make_load_args(filename, N)
    plot_args = make_plot_args(label, linestyle=linestyle, color=color)

    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)
        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, 0],
            mean_values=mean_data[:, 1],
            std_values=std_data[:, 1],
            **plot_args,
        )
    else:
        data = load_data(**load_args, skip_header=0)
        ax.plot(data[:, 0], data[:, 1], **plot_args)

    format_axis(
        ax,
        ref,
        fontsize,
        xlabel=styles.getArcLengthLabel(),
        ylabel=styles.getHeadLabel(3),
        title=title if kwargs.get("show_title", False) else None,
        show_legend=kwargs.get("show_legend", False),
        xlim=kwargs.get("xlim", None),
        ylim=kwargs.get("ylim", None),
    )


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
    N = 9
    load_args = make_load_args(filename, N)
    plot_args = make_plot_args(label, linestyle=linestyle, color=color)

    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)

        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, 0],
            mean_values=mean_data[:, ID + 1],
            std_values=std_data[:, ID + 1],
            **plot_args,
        )
    else:
        data = load_data(**load_args, skip_header=0)
        ax.plot(data[:, 0], data[:, ID + 1], **plot_args)

    format_axis(
        ax,
        ref,
        fontsize,
        xlabel=styles.getTimeLabel("s"),
        ylabel=r"$\overline{c_2}$",
        title=title if kwargs.get("show_title", False) else None,
        show_legend=kwargs.get("show_legend", False),
        xlim=kwargs.get("xlim", None),
        ylim=kwargs.get("ylim", None),
    )


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
