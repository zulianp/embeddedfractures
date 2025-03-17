import sys

import numpy as np
from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *

# Plot IDs for line plots
id_p_matrix = 0  # pressure along (0, 100, 100)-(100, 0, 0)
id_p_matrix_legend = 10
id_c_matrix = 1  # c along (0, 100, 100)-(100, 0, 0)
id_c_matrix_legend = 11
id_c_fracture = 2  # c along (0, 100, 80)-(100, 0, 20)
id_c_fracture_legend = 12

# Plot IDs for time plots
id_intc_matrix = 0  # integral of c*porosity in the lower matrix sub-domain
id_intc_matrix_legend = 10
id_intc_fracture = 1  # integral of c*porosity in the fracture
id_intc_fracture_legend = 11
id_outflux = 2  # integrated outflux across the outflow boundary
id_outflux_legend = 12


def plot_legend_in_middle(ax, fontsize=30):
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=4,
        fontsize=fontsize,
    )


def plot_over_line(
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
    N = 5
    if "mean" in filename:
        std_filename = filename.replace("mean", "std")
        mean_data = np.genfromtxt(
            filename,
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
        if mean_data.shape != std_data.shape:
            raise ValueError(
                "Mean and standard deviation data do not have the same shape!"
            )
        ax.fill_between(
            mean_data[:, 2 * ID],
            mean_data[:, 2 * ID + 1] - std_data[:, 2 * ID + 1],
            mean_data[:, 2 * ID + 1] + std_data[:, 2 * ID + 1],
            color=color,
            alpha=0.5,
        )
        ax.plot(
            mean_data[:, 2 * ID],
            mean_data[:, 2 * ID + 1],
            label=label,
            linestyle=linestyle,
            color=color,
        )
    else:
        data = np.genfromtxt(
            filename, delimiter=",", converters=dict(zip(range(N), [c] * N))
        )
        ax.plot(
            data[:, 2 * ID],
            data[:, 2 * ID + 1],
            label=label,
            linestyle=linestyle,
            color=color,
        )

    format_axis(ax, ref, fontsize)
    ax.set_xlabel(styles.getArcLengthLabel(), fontsize=fontsize)
    ax.grid(True)
    if kwargs.get("show_title", True):
        ax.set_title(title, fontsize=fontsize)
    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))
    ylabel_map = {
        id_p_matrix: styles.getHeadLabel(3),
        id_c_matrix: styles.getConcentrationLabel(3),
        id_c_fracture: styles.getConcentrationLabel(2),
    }
    if ID in ylabel_map:
        ax.set_ylabel(ylabel_map[ID], fontsize=fontsize)
    else:
        print("Error: Invalid plot id provided.")
        sys.exit(1)


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
    N = 4
    if "mean" in filename:
        std_filename = filename.replace("mean", "std")
        mean_data = np.genfromtxt(
            filename,
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
        if mean_data.shape != std_data.shape:
            raise ValueError(
                "Mean and standard deviation data do not have the same shape!"
            )
        time = mean_data[:, 0] / (365 * 24 * 3600)
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
        time = data[:, 0] / (365 * 24 * 3600)
        ax.plot(time, data[:, ID + 1], label=label, linestyle=linestyle, color=color)

    format_axis(ax, ref, fontsize)
    ax.set_xlabel(styles.getTimeLabel("y"), fontsize=fontsize)
    ax.grid(True)
    if kwargs.get("show_title", True):
        ax.set_title(title, fontsize=fontsize)
    if kwargs.get("show_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))
    if kwargs.get("xlim") is not None:
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim") is not None:
        ax.set_ylim(kwargs.get("ylim"))
    ylabel_map = {
        id_intc_matrix: r"$\int_{\Omega_3} \phi_3 \, c_3$",
        id_intc_fracture: r"$\int_{\Omega_2} \phi_2 \, c_2$",
        id_outflux: "outflux",
    }
    if ID in ylabel_map:
        ax.set_ylabel(ylabel_map[ID], fontsize=fontsize)
    else:
        print("Error: Invalid plot id provided.")
        sys.exit(1)


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1, fontsize=30):
    import matplotlib.pyplot as plt

    plt.figure(ID + 11)  # Workaround for figure ID issues
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol, fontsize=fontsize)


def plot_percentiles(ref, ID, places_and_methods, ax, fontsize=30, **kwargs):
    paths = get_paths(__file__)
    c = lambda s: float(s.decode().replace("D", "e"))
    N = 6

    format_axis(ax, ref, fontsize)

    funcs, minX, maxX = [], -np.inf, np.inf
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
            data = data[:, 2 * ID : 2 * ID + 2]
            data = data[~np.isnan(data).any(axis=1)]
            funcs.append(interpolate.interp1d(data[:, 0], data[:, 1]))
            minX = max(minX, data[0, 0])
            maxX = min(maxX, data[-1, 0])
    ls = np.linspace(minX, maxX, num=1000)
    interpolated = [f(ls) for f in funcs]
    meanvalues = np.mean(interpolated, axis=0)
    upperpercentile = np.percentile(interpolated, 90, axis=0)
    lowerpercentile = np.percentile(interpolated, 10, axis=0)

    ax.fill_between(ls, lowerpercentile, upperpercentile, color="gray")
    ax.grid(True)
    ax.set_xlabel(styles.getArcLengthLabel(), fontsize=fontsize)
    weightedarea = (simps(upperpercentile, ls) - simps(lowerpercentile, ls)) / simps(
        meanvalues, ls
    )
    ax.set_title("weighted area " + MathTextSciFormatter("%1.2e")(weightedarea))
    if kwargs.get("ylim") is not None:
        ax.set_ylim(kwargs.get("ylim"))

    ylabel_map = {
        id_p_matrix: styles.getHeadLabel(3),
        id_c_matrix: styles.getConcentrationLabel(3),
        id_c_fracture: styles.getConcentrationLabel(2),
    }
    if ID in ylabel_map:
        ax.set_ylabel(ylabel_map[ID], fontsize=fontsize)
    else:
        print("Error. Invalid plot id provided.")
        sys.exit(1)

    return ls, lowerpercentile, upperpercentile

