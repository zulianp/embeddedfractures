# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from __future__ import print_function

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

os.environ['PATH'] += ':/Library/TeX/texbin'
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

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

#------------------------------------------------------------------------------#
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=15)

# ids of the different plots
id_p_0_matrix = 0   # pressure along (0, 100, 100)-(100, 0, 0)
id_p_0_matrix_legend = 10   # pressure along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix = 1   # p along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix_legend = 11   # p along (0, 100, 100)-(100, 0, 0)
id_pot = 2
id_pot_legend = 12   # p along (0, 100, 100)-(100, 0, 0)

linestyle = styles.linestyle
color = styles.color

curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
case = curr_dir.split(os.sep)[-1] # case we are dealing with

def plot_legend_in_middle(ax):
    handles, labels = ax.get_legend_handles_labels()

    if isinstance(ax, (list, np.ndarray)):  # Check if it's an array of subplots
        mid_ax = ax[len(ax) // 2]  # Select the middle axis for the legend
        mid_ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=4, fontsize=14)
    else:  # Single plot
        ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize=14)  # Adjust for a sin

def setup_figure(id_offset, num_axes, ylim):
    fig = plt.figure(id_offset + 11, figsize=(16, 8))  # Increased figure height to accommodate the legend
    fig.subplots_adjust(hspace=0.4, wspace=0)  # Increase space between plots vertically
    axes_list = [fig.add_subplot(1, num_axes, idx + 1, ylim=ylim) for idx in range(num_axes)]
    return fig, axes_list

def plot_over_line(file_name, legend, ID, title, ax, linestyle='-', color='C0', **kwargs):
    # Define the converter for the input data
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 2  # Assumes the number of columns is 2 for regular data

    # Check if the file_name contains 'mean' to determine if we're plotting mean and std
    if 'mean' in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace('mean', 'std')

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c] * N)))
        std_data = np.genfromtxt(std_filename, delimiter=",", converters=dict(zip(range(N), [c] * N)))

        # Ensure that the mean and std arrays have consistent shapes
        if mean_data.shape != std_data.shape:
            raise ValueError("Mean and standard deviation data do not have the same shape!")

        # Plot standard deviation band (mean +/- std)
        ax.fill_between(mean_data[:, 0],
                        mean_data[:, 1] - std_data[:, 1],
                        mean_data[:, 1] + std_data[:, 1],
                        color=color, alpha=0.3)  # Adjust transparency for visibility

        # Plot the mean data line
        ax.plot(mean_data[:, 0], mean_data[:, 1], label=legend, linestyle=linestyle, color=color)
    else:
        # Plot only the mean data
        data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c] * N)))
        ax.plot(data[:, 0], data[:, 1], label=legend, linestyle=linestyle, color=color)

    # Format y-axis using scientific notation
    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

    # Set x-axis label and grid
    ax.set_xlabel(styles.getArcLengthLabel())
    ax.grid(True)
    ax.set_ylabel(styles.getHeadLabel(3))

    # Set plot title if needed
    if kwargs.get("has_title", True):
        ax.set_title(title)

    # Set legend if needed
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Set xlim and ylim if provided
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))

    # Set specific ticks depending on the ID
    if ID == id_p_0_matrix:
        ax.set_xticks([0, 500, 1000, 1500])
        ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700])
    elif ID == id_p_1_matrix:
        ax.set_xticks([0, 500, 1000, 1500])
        ax.set_yticks([0, 50, 100, 150, 200, 250])

def save(simulation_id, filename, extension=".pdf", ax_title=None):
    os.makedirs(plots_dir, exist_ok=True)

    fig = plt.figure(simulation_id+11)

    for idx, ax in enumerate(fig.get_axes()):
        ax.label_outer()
        if len(fig.get_axes()) > 1:
            text = "\\textbf{subfig. " + chr(97+idx) + "}"
            ax.text(0.5, -0.2, text, horizontalalignment='center',
                    verticalalignment='bottom', transform=ax.transAxes)
        elif ax_title is not None:
            ax.text(0.5, -0.25, ax_title, horizontalalignment='center',
                    verticalalignment='bottom', transform=ax.transAxes)

    plt.savefig(os.path.join(plots_dir, filename+extension), bbox_inches='tight')
    plt.gcf().clear()

def crop_pdf(filename):
    filename = os.path.join(plots_dir, filename + ".pdf")
    if os.path.isfile(filename):
        os.system("pdfcrop --margins '0 -300 0 0' " + filename + " " + filename)
        os.system("pdfcrop " + filename + " " + filename)


def plot_over_time(file_name, legend, title, ID, region, region_pos, num_regions, ax, linestyle='-', color='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 53  # Number of columns in the file

    # Check if the file_name contains 'mean' to determine if we're plotting mean and std
    if 'mean' in file_name:
        # Generate the std filename by replacing 'mean' with 'std'
        std_filename = file_name.replace('mean', 'std')

        # Read mean and standard deviation data from files
        mean_data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c] * N)))
        std_data = np.genfromtxt(std_filename, delimiter=",", converters=dict(zip(range(N), [c] * N)))

        # Time and values for mean and std
        time = mean_data[:, 0]
        mean_values = mean_data[:, region + 1]
        std_values = std_data[:, region + 1]

        # Plot the mean with a shaded region for the standard deviation
        ax.fill_between(time, mean_values - std_values, mean_values + std_values, color=color, alpha=0.3)
        ax.plot(time, mean_values, label=legend, linestyle=linestyle, color=color)
    else:
        # Plot the regular data
        data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c] * N)))
        time = data[:, 0]
        values = data[:, region + 1]
        ax.plot(time, values, label=legend, linestyle=linestyle, color=color)

    # Format y-axis using scientific notation
    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))
    plt.rcParams.update({'figure.max_open_warning': 0})

    # Remove y-axis ticks if region_pos is set
    if region_pos > 0:
        ax.yaxis.set_tick_params(length=0)

    # Set x-axis label and grid
    ax.set_xlabel(styles.getTimeLabel('s'))
    ax.set_ylabel(styles.getAveragedConcentrationLabel(2))
    ax.grid(True)

    # Set plot title if needed
    if kwargs.get("has_title", True):
        ax.set_title(title)

    # Set legend if needed
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Set xlim and ylim if provided
    if kwargs.get("xlim", None):
        plt.xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))

    # Set specific xticks
    ax.set_xticks([0, 500, 1000, 1500])



def save_over_time(filename, extension=".pdf"):
    os.makedirs(plots_dir, exist_ok=True)

    for ID in np.arange(52):
        plt.figure(ID)
        plt.savefig(os.path.join(plots_dir, filename+"_fracture_"+str(ID)+extension), bbox_inches='tight')
        plt.gcf().clear()

def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1):
    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID+11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol)

class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2e"):
        self.fmt = fmt
    def __call__(self, x, pos=None):
        s = self.fmt % x
        if "f" in self.fmt:
            return "${}$".format(s)
        decimal_point = '.'
        positive_sign = '+'
        tup = s.split('e')
        significand = tup[0].rstrip(decimal_point)
        sign = tup[1][0].replace(positive_sign, '')
        exponent = tup[1][1:].lstrip('0')
        if exponent:
            exponent = '10^{%s%s}' % (sign, exponent)
        if significand and exponent:
            s =  r'%s{\times}%s' % (significand, exponent)
        else:
            s =  r'%s%s' % (significand, exponent)
        return "${}$".format(s)

def plot_percentiles(ref, places_and_methods, ax, **kwargs):

    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 2

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    f = []
    minX = -np.inf
    maxX = np.inf

    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method)
            datafile = os.path.join(folder, f"dol_line_{ref}.csv").replace("\_", "_")
            data = np.genfromtxt(datafile, delimiter=",", converters=dict(zip(range(N), [c]*N)))
            # only take the interesting columns and eleminate nan rows
            data = data[:, 0:2]
            data = data[~np.isnan(data).any(axis=1)]

            f.append(interpolate.interp1d(data[:, 0], data[:, 1]))
            minX = max(minX, data[0, 0])
            maxX = min(maxX, data[-1, 0])

    ls = np.linspace(minX, maxX, num=1000)
    interpolateddata = list(map(methodcaller('__call__', ls), f))
    meanvalues = np.mean(interpolateddata, axis=0)
    variance = np.var(interpolateddata, axis=0)
    lowerpercentile = np.percentile(interpolateddata, 10, axis=0)
    upperpercentile = np.percentile(interpolateddata, 90, axis=0)

    ax.fill_between(ls, lowerpercentile, upperpercentile, color="gray")
    ax.grid(True)
    ax.set_xlabel( styles.getArcLengthLabel() )
    weightedarea = (simps(upperpercentile, ls) -
                    simps(lowerpercentile, ls))/simps(meanvalues, ls)
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
    ax.set_ylabel( styles.getHeadLabel(3) )

    return (ls, lowerpercentile, upperpercentile)
