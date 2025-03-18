# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from operator import methodcaller

from scipy import interpolate
from scipy.integrate import simps

from fracture_plotter.utils.general import get_paths
from fracture_plotter.utils.plot_routines_utils import *


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
