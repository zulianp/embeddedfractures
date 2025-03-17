import sys

import numpy as np
from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *

paths = get_paths(__file__)

# Plot IDs
id_p_matrix, id_c_matrix, id_c_fracture = 0, 1, 2
id_intc_matrix, id_intc_fracture, id_outflux = 0, 1, 2


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
    N = 5
    load_args = make_load_args(filename, N)
    plot_args = make_plot_args(label, linestyle, color)
    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)
        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, 2 * ID],
            mean_values=mean_data[:, 2 * ID + 1],
            std_values=std_data[:, 2 * ID + 1],
            **plot_args,
        )
    else:
        data = load_data(**load_args, skip_header=0)
        ax.plot(data[:, 2 * ID], data[:, 2 * ID + 1], **plot_args)

    ylabel = {
        id_p_matrix: styles.getHeadLabel(3),
        id_c_matrix: styles.getConcentrationLabel(3),
        id_c_fracture: styles.getConcentrationLabel(2),
    }.get(ID)

    format_axis(
        ax,
        ref,
        fontsize,
        xlabel=styles.getArcLengthLabel(),
        ylabel=ylabel,
        title=title if kwargs.get("show_title", False) else None,
        show_legend=kwargs.get("show_legend", False),
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
    N = 4
    load_args = make_load_args(filename, N)
    plot_args = make_plot_args(label, linestyle, color)

    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)
        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, 0] / (365 * 24 * 3600),
            mean_values=mean_data[:, ID + 1],
            std_values=std_data[:, ID + 1],
            **plot_args,
        )
    else:
        data = load_data(**load_args, skip_header=0)
        ax.plot(data[:, 0] / (365 * 24 * 3600), data[:, ID + 1], **plot_args)

    ylabel = {
        id_intc_matrix: r"$\int_{\Omega_3} \phi_3 \, c_3$",
        id_intc_fracture: r"$\int_{\Omega_2} \phi_2 \, c_2$",
        id_outflux: "outflux",
    }.get(ID)

    if ylabel is None:
        sys.exit("Error: Invalid plot id provided.")

    format_axis(
        ax,
        ref,
        fontsize,
        xlabel=styles.getTimeLabel("y"),
        ylabel=ylabel,
        title=title if kwargs.get("show_title", False) else None,
        show_legend=kwargs.get("show_legend", False),
        xlim=kwargs.get("xlim", None),
        ylim=kwargs.get("ylim", None),
    )


def plot_percentiles(ref, ID, places_and_methods, ax, fontsize=30, ylim=None):
    c, N = lambda s: float(s.decode().replace("D", "e")), 6
    format_axis(ax, ref, fontsize)

    funcs, minX, maxX = [], -np.inf, np.inf
    for place, methods in places_and_methods.items():
        if place == "DTU" and ID != id_p_matrix:
            continue
        for method in methods:
            datafile = os.path.join(
                paths.results_dir, place, method, f"dol_refinement_{ref}.csv"
            ).replace("\_", "_")
            data = np.genfromtxt(
                datafile, delimiter=",", converters={i: decode_float for i in range(N)}
            )
            data = data[:, 2 * ID : 2 * ID + 2]
            data = data[~np.isnan(data).any(axis=1)]
            funcs.append(interpolate.interp1d(data[:, 0], data[:, 1]))
            minX, maxX = max(minX, data[0, 0]), min(maxX, data[-1, 0])

    ls = np.linspace(minX, maxX, 1000)
    interpolated = [f(ls) for f in funcs]
    meanvalues = np.mean(interpolated, axis=0)
    lower, upper = np.percentile(interpolated, [10, 90], axis=0)

    ax.fill_between(ls, lower, upper, color="gray")
    ax.grid(True)
    ax.set_xlabel(styles.getArcLengthLabel(), fontsize=fontsize)
    weighted_area = (simps(upper, ls) - simps(lower, ls)) / simps(meanvalues, ls)
    ax.set_title(f"weighted area {MathTextSciFormatter('%1.2e')(weighted_area)}")

    if ylim:
        ax.set_ylim(ylim)

    ylabel = {
        id_p_matrix: styles.getHeadLabel(3),
        id_c_matrix: styles.getConcentrationLabel(3),
        id_c_fracture: styles.getConcentrationLabel(2),
    }.get(ID)

    if ylabel is None:
        sys.exit("Error: Invalid plot id provided.")

    ax.set_ylabel(ylabel, fontsize=fontsize)
    return ls, lower, upper
