# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from __future__ import print_function

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from scipy import interpolate
from scipy.integrate import simps
from operator import methodcaller

import numpy as np
import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = curr_dir.replace('scripts', 'plots')
results_dir = curr_dir.replace('scripts', 'results')
utils_dir = os.path.abspath(os.path.join(curr_dir, '../utils'))
sys.path.insert(0, utils_dir)
import styles

# ------------------------------------------------------------------------------#

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=15)

# ids of the different plots
id_p_matrix = 0  # pressure along (0, 100, 100)-(100, 0, 0)
id_p_matrix_legend = 10  # pressure along (0, 100, 100)-(100, 0, 0)
id_c_matrix = 1  # c along (0, 100, 100)-(100, 0, 0)
id_c_matrix_legend = 11  # c along (0, 100, 100)-(100, 0, 0)
id_c_fracture = 2  # c along (0, 100, 80)-(100, 0, 20)
id_c_fracture_legend = 12  # c along (0, 100, 80)-(100, 0, 20)

linestyle = styles.linestyle
color = styles.color

curr_dir = os.path.dirname(os.path.realpath(__file__))  # current directory
case = curr_dir.split(os.sep)[-1]  # case we are dealing with

def setup_figure(id_offset, num_axes, ylim):
    fig = plt.figure(id_offset + 11, figsize=(16, 8))  # Increased figure height to accommodate the legend
    fig.subplots_adjust(hspace=0.4, wspace=0)  # Increase space between plots vertically
    axes_list = [fig.add_subplot(1, num_axes, idx + 1, ylim=ylim) for idx in range(num_axes)]
    return fig, axes_list

def get_paths():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = curr_dir.replace('scripts', 'plots')
    results_dir = curr_dir.replace('scripts', 'results')
    utils_dir = os.path.join(curr_dir, 'utils')
    return curr_dir, plots_dir, results_dir, utils_dir


def plot_over_line(file_name, legend, ref, ID, title, ax, linestyle='-', color='C0', **kwargs):
    # Define the converter for the input data
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 5  # Assumes the number of columns is 5

    # Check if the file_name contains 'mean' to determine if we're plotting mean and std
    if 'mean' in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace('mean', 'std')

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(file_name, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c] * N)))
        std_data = np.genfromtxt(std_filename, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c] * N)))

        # Ensure that the mean and std arrays have consistent shapes
        if mean_data.shape != std_data.shape:
            raise ValueError("Mean and standard deviation data do not have the same shape!")

        # Plot standard deviation band (mean +/- std)
        ax.fill_between(mean_data[:, 2 * ID],
                        mean_data[:, 2 * ID + 1] - std_data[:, 2 * ID + 1],
                        mean_data[:, 2 * ID + 1] + std_data[:, 2 * ID + 1],
                        color=color, alpha=0.5)  # Adjust transparency for visibility

        # Plot the mean data line
        ax.plot(mean_data[:, 2 * ID], mean_data[:, 2 * ID + 1], label=legend, linestyle=linestyle, color=color)
    else:
        # Plot only the mean data
        data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c] * N)))
        ax.plot(data[:, 2 * ID], data[:, 2 * ID + 1], label=legend, linestyle=linestyle, color=color)

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


def save(ID, filename, extension=".pdf", **kwargs):
    os.makedirs(plots_dir, exist_ok=True)

    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    fig = plt.figure(ID + 11)

    for idx, ax in enumerate(fig.get_axes()):
        ax.label_outer()
        if len(fig.get_axes()) > 1:
            index = 97 + idx + kwargs.get("starting_from", 0)
            text = "\\textbf{subfig. " + chr(index) + "}"
            ax.text(0.5, -0.2, text, horizontalalignment='center',
                    verticalalignment='bottom', transform=ax.transAxes)

    plt.savefig(os.path.join(plots_dir, filename + extension), bbox_inches='tight')
    plt.gcf().clear()


def crop_pdf(filename):
    filename = os.path.join(plots_dir, filename + ".pdf")
    if os.path.isfile(filename):
        os.system("pdfcrop --margins '0 -300 0 0' " + filename + " " + filename)
        os.system("pdfcrop " + filename + " " + filename)


# ids of the different plots
id_intc_matrix = 0  # integral of c*porosity in the lower matrix sub-domain
id_intc_matrix_legend = 10  # integral of c*porosity in the lower matrix sub-domain
id_intc_fracture = 1  # indegral of c*porosity in the fracture
id_intc_fracture_legend = 11  # indegral of c*porosity in the fracture
id_outflux = 2  # integrated outflux across the outflow boundary
id_outflux_legend = 12  # integrated outflux across the outflow boundary

def plot_over_time(file_name, legend, ref, ID, title, ax, linestyle='-', color='C0', **kwargs):
    # Define the converter for the input data
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 4  # Assumes the number of columns is 4

    # Check if the file_name contains 'mean' to determine if we're plotting mean and std
    if 'mean' in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace('mean', 'std')

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(file_name, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c] * N)))
        std_data = np.genfromtxt(std_filename, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c] * N)))

        # Ensure that the mean and std arrays have consistent shapes
        if mean_data.shape != std_data.shape:
            raise ValueError("Mean and standard deviation data do not have the same shape!")

        time = mean_data[:, 0] / (365 * 24 * 3600)  # Convert time to years
        mean_values = mean_data[:, ID + 1]
        std_values = std_data[:, ID + 1]

        # Plot the mean with a shaded region for the standard deviation
        ax.fill_between(time, mean_values - std_values, mean_values + std_values, color=color, alpha=0.3)
        ax.plot(time, mean_values, label=legend, linestyle=linestyle, color=color)
    else:
        # Plot only the mean data
        data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c] * N)))
        time = data[:, 0] / (365 * 24 * 3600)  # Convert time to years
        ax.plot(time, data[:, ID + 1], label=legend, linestyle=linestyle, color=color)

    # Format y-axis using scientific notation
    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    # Remove y-axis ticks if ref is set
    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    # Set x-axis label and grid
    ax.set_xlabel(styles.getTimeLabel('y'))
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
    def __init__(self, fmt="%1.2e"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        decimal_point = '.'
        positive_sign = '+'
        tup = s.split('e')
        significand = tup[0].rstrip(decimal_point)
        sign = tup[1][0].replace(positive_sign, '')
        exponent = tup[1][1:].lstrip('0')
        if exponent:
            exponent = '10^{%s%s}' % (sign, exponent)
        if significand and exponent:
            s = r'%s{\times}%s' % (significand, exponent)
        else:
            s = r'%s%s' % (significand, exponent)
        return "${}$".format(s)


def plot_percentiles(ref, ID, places_and_methods, ax, **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
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
            folder = os.path.join(results_dir, place, method)
            datafile = os.path.join(folder, f"dol_refinement_{ref}.csv").replace("\_", "_")
            data = np.genfromtxt(datafile, delimiter=",", converters=dict(zip(range(N), [c] * N)))
            # only take the interesting columns and eleminate nan rows
            data = data[:, 2 * ID:2 * ID + 2];
            data = data[~np.isnan(data).any(axis=1)]

            f.append(interpolate.interp1d(data[:, 0], data[:, 1]))
            minX = max(minX, data[0, 0])
            maxX = min(maxX, data[-1, 0])

    ls = np.linspace(minX, maxX, num=1000)
    interpolateddata = list(map(methodcaller('__call__', ls), f))
    meanvalues = np.mean(interpolateddata, axis=0)
    variance = np.var(interpolateddata, axis=0)
    upperpercentile = np.percentile(interpolateddata, 90, axis=0)
    lowerpercentile = np.percentile(interpolateddata, 10, axis=0)

    ax.fill_between(ls, lowerpercentile, upperpercentile, color="gray")
    ax.grid(True)
    ax.set_xlabel(styles.getArcLengthLabel())
    weightedarea = (simps(upperpercentile, ls) -
                    simps(lowerpercentile, ls)) / simps(meanvalues, ls)
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

