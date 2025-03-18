import sys

import numpy as np
from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *

paths = get_paths(__file__)


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
