# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
from __future__ import print_function

import matplotlib as mpl
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

#------------------------------------------------------------------------------#

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=15)

# ids of the different plots
id_p_0_matrix = 0   # pressure along (0, 100, 100)-(100, 0, 0)
id_p_0_matrix_legend = 10   # pressure along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix = 1   # p along (0, 100, 100)-(100, 0, 0)
id_p_1_matrix_legend = 11   # p along (0, 100, 100)-(100, 0, 0)
id_pot_legend = 12   # p along (0, 100, 100)-(100, 0, 0)

linestyle = styles.linestyle
color = styles.color

curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
case = curr_dir.split(os.sep)[-1] # case we are dealing with

def plot_over_line(file_name, legend, ref, ID, title, ax, linestyle='-', color='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 2
    data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c]*N)))

    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    ax.plot(data[:, 0], data[:, 1], label=legend, linestyle=linestyle, color=color)
    ax.set_xlabel( styles.getArcLengthLabel() )
    ax.grid(True)
    if kwargs.get("has_title", True):
        ax.set_title(title)
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))
    if kwargs.get("xlim", None):
        plt.xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))

    ax.set_ylabel(styles.getHeadLabel(3))

def plot_mean_and_std_over_line(mean_filename, std_filename, legend, ref, ID, title, ax, linestyle='-', color='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 2

    # Read the mean and standard deviation data
    mean_data = np.genfromtxt(mean_filename, delimiter=",", converters=dict(zip(range(N), [c]*N)))
    std_data = np.genfromtxt(std_filename, delimiter=",", converters=dict(zip(range(N), [c]*N)))

    # Set y-axis format
    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

    # Remove y-axis ticks if reference is non-zero
    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    # Fill between the mean ± std values
    ax.fill_between(mean_data[:, 0], 
                    mean_data[:, 1] - std_data[:, 1], 
                    mean_data[:, 1] + std_data[:, 1], 
                    color=color, alpha=0.3)

    # Plot the mean line
    ax.plot(mean_data[:, 0], mean_data[:, 1], label=legend, linestyle=linestyle, color=color)

    # Set x-axis label and grid
    ax.set_xlabel(styles.getArcLengthLabel())
    ax.grid(True)

    # Set optional title and legend
    if kwargs.get("has_title", True):
        ax.set_title(title)
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Set optional x and y limits
    if kwargs.get("xlim", None):
        plt.xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))

    # Set y-axis label
    ax.set_ylabel(styles.getHeadLabel(3))

def save(simulation_id, filename, extension=".pdf"):
    os.makedirs(plots_dir, exist_ok=True)

    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    fig = plt.figure(simulation_id+11)

    for idx, ax in enumerate(fig.get_axes()):
        ax.label_outer()
        if len(fig.get_axes()) > 1:
            text = "\\textbf{subfig. " + chr(97+idx) + "}"
            ax.text(0.5, -0.2, text, horizontalalignment='center',
                    verticalalignment='bottom', transform=ax.transAxes)

    plt.savefig(os.path.join(plots_dir, filename+extension), bbox_inches='tight')
    plt.gcf().clear()

def crop_pdf(filename):
    filename = os.path.join(plots_dir, filename + ".pdf")
    if os.path.isfile(filename):
        os.system("pdfcrop --margins '0 -300 0 0' " + filename + " " + filename)
        os.system("pdfcrop " + filename + " " + filename)


def plot_over_time(file_name, legend, ref, ID, title, ax, linestyle='-', color='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 9
    data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c]*N)))

    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    ax.plot(data[:, 0], data[:, ID+1], label=legend, linestyle=linestyle, color=color)
    ax.set_xlabel( styles.getTimeLabel('s') )
    ax.grid(True)

    if kwargs.get("has_title", True):
        title_fig = title + " - fracture " + str(ID)
        ax.set_title(title_fig)
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    ax.set_ylabel(r"$\overline{c_2}$")

    if kwargs.get("xlim", None):
        plt.xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))


def plot_mean_and_std_over_time(mean_filename, std_filename, legend, ref, ID, title, ax, linestyle='-', color='C0', **kwargs):
    # Converter to handle scientific notation
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 9

    # Read the mean and standard deviation data
    mean_data = np.genfromtxt(mean_filename, delimiter=",", converters=dict(zip(range(N), [c]*N)))
    std_data = np.genfromtxt(std_filename, delimiter=",", converters=dict(zip(range(N), [c]*N)))

    # Format y-axis with the provided or default format
    ax.yaxis.set_major_formatter(MathTextSciFormatter(kwargs.get("fmt", "%1.2e")))

    # Adjust y-axis tick marks if `ref` is specified
    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    # Extract time, mean, and standard deviation values
    time = mean_data[:, 0]
    mean_values = mean_data[:, ID + 1]
    std_values = std_data[:, ID + 1]

    # Plot the shaded region (mean ± std) and the mean line
    ax.fill_between(time, mean_values - std_values, mean_values + std_values, color=color, alpha=0.3)
    ax.plot(time, mean_values, label=legend, linestyle=linestyle, color=color)

    # Set x-axis label using `styles.getTimeLabel`
    ax.set_xlabel(styles.getTimeLabel('s'))
    
    # Display grid
    ax.grid(True)

    # Optionally set the title
    if kwargs.get("has_title", True):
        title_fig = title + " - fracture " + str(ID)
        ax.set_title(title_fig)

    # Optionally display the legend
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # Set y-label as specified in the original function
    ax.set_ylabel(r"$\overline{c_2}$")

    # Apply optional xlim and ylim if provided in kwargs
    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))


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


def save_over_time(filename, extension=".pdf"):
    for ID in np.arange(8):
        save(ID, filename+"_fracture_"+str(ID), extension=extension)

def plot_boundary_data(data, methods, data_ref, colors, linestyle, extension=".pdf"):
    plot_boundary_head(data[:, 4:], methods, data_ref[2], colors, linestyle, extension)
    plot_boundary_fluxes(data[:, :4], methods, data_ref[1], colors, linestyle, extension)
    plot_reference_fluxes(data[:, :4], methods, data_ref[1], colors, linestyle, extension)


def plot_boundary_fluxes(da, methods, ratio_ref, colors, linestyle, extension):
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
        ax.bar(ind + width * i, da[:, i+2], width, color=c, edgecolor="white")

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
    os.makedirs(plots_dir, exist_ok=True)

    text = "\\textbf{subfig. b}"
    ax.text(0.5, -0.2, text, horizontalalignment='center',
            verticalalignment='bottom', transform=ax.transAxes)

    plt.savefig(os.path.join(plots_dir, f"{case}_boundary_head" + extension), bbox_inches="tight")

def plot_reference_fluxes(da, methods, ratio_ref, colors, linestyle, extension):
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
    os.makedirs(plots_dir, exist_ok=True)

    text = "\\textbf{subfig. a}"
    ax.text(0.5, -0.2, text, horizontalalignment='center',
            verticalalignment='bottom', transform=ax.transAxes)

    plt.savefig(os.path.join(plots_dir, f"{case}_reference_flux" + extension), bbox_inches="tight")


def plot_boundary_head(da, methods, head_ref, colors, linestyle, extension):
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
        ax.bar(ind + width * i, da[:, i], width, color=c, edgecolor='white')#, hatch=linestyle)

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

    os.makedirs(plots_dir, exist_ok=True)

    text = "\\textbf{subfig. c}"
    ax.text(0.5, -0.2, text, horizontalalignment='center',
            verticalalignment='bottom', transform=ax.transAxes)

    plt.savefig(os.path.join(plots_dir, f"{case}_boundary_fluxes" + extension), bbox_inches="tight")

def plot_percentiles(ref, line_id, places_and_methods, ax, **kwargs):

    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 2

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    f = []
    minX = -np.inf
    maxX = np.inf

    for place in places_and_methods:
        for method in places_and_methods[place]:
            base_dir = os.getcwd().replace("scripts", "results")
            folder = os.path.join(base_dir, place, method)
            datafile = os.path.join(folder, "dol_line_" + line_id + "_refinement_" + ref + ".csv").replace("\_", "_")
            data = np.genfromtxt(datafile, delimiter=",", converters=dict(zip(range(N), [c]*N)))
            data = data[:, 0:2];
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
    ax.set_xlabel( styles.getArcLengthLabel() )
    weightedarea = (simps(upperpercentile, ls) -
                    simps(lowerpercentile, ls))/simps(meanvalues, ls)
    title = "weighted area " + MathTextSciFormatter("%1.2e")(weightedarea)
    ax.title.set_text(title)
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))

    ax.set_ylabel( styles.getHeadLabel(3) )

    return (ls, lowerpercentile, upperpercentile)

