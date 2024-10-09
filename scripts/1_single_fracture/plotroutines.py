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
curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
case = curr_dir.split(os.sep)[-1] # case we are dealing with
utils_dir = os.path.abspath(os.path.join(curr_dir, '../utils'))
sys.path.insert(0, utils_dir)
import styles
from plot_routines_utils import *

#------------------------------------------------------------------------------#

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=15)

# ids of the different plots
id_p_matrix = 0   # pressure along (0, 100, 100)-(100, 0, 0)
id_p_matrix_legend = 10   # pressure along (0, 100, 100)-(100, 0, 0)
id_c_matrix = 1   # c along (0, 100, 100)-(100, 0, 0)
id_c_matrix_legend = 11   # c along (0, 100, 100)-(100, 0, 0)
id_c_fracture = 2 # c along (0, 100, 80)-(100, 0, 20)
id_c_fracture_legend = 12 # c along (0, 100, 80)-(100, 0, 20)

linestyle = styles.linestyle
color = styles.color

def plot_over_line(file_name, legend, ref, ID, title, ax, lineStyle='-', clr='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 5

    data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c]*N)))

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    ax.plot(data[:, 2*ID], data[:, 2*ID+1], label=legend, linestyle=lineStyle, color=clr)
    ax.set_xlabel( styles.getArcLengthLabel() )
    ax.grid(True)
    if kwargs.get("has_title", True):
        ax.set_title(title)
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))

    # choose y-label depending on plot id
    if ID == id_p_matrix:
        ax.set_ylabel( styles.getHeadLabel(3) )
    elif ID == id_c_matrix:
        ax.set_ylabel( styles.getConcentrationLabel(3) )
    elif ID == id_c_fracture:
        ax.set_ylabel( styles.getConcentrationLabel(2) )
    else:
        print("Error. Invalid plot id provided.")
        sys.exit(1)

def plot_mean_and_std_over_line(mean_filename, std_filename, legend, ref, ID, title, ax, lineStyle='-', clr='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 5

    # Read the mean and standard deviation data
    mean_data = np.genfromtxt(mean_filename, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c]*N)))
    std_data = np.genfromtxt(std_filename, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c]*N)))

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    # Corrected x-axis values in fill_between
    ax.fill_between(mean_data[:, 2*ID], mean_data[:, 2*ID+1] - std_data[:, 2*ID+1], mean_data[:, 2*ID+1] + std_data[:, 2*ID+1], color=clr, alpha=0.3)
    ax.plot(mean_data[:, 2*ID], mean_data[:, 2*ID+1], label=legend, linestyle=lineStyle, color=clr)
    ax.set_xlabel(styles.getArcLengthLabel())
    ax.grid(True)
    if kwargs.get("has_title", True):
        ax.set_title(title)
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
        print("Error. Invalid plot id provided.")
        sys.exit(1)

# ids of the different plots
id_intc_matrix = 0   # integral of c*porosity in the lower matrix sub-domain
id_intc_matrix_legend = 10   # integral of c*porosity in the lower matrix sub-domain
id_intc_fracture = 1 # indegral of c*porosity in the fracture
id_intc_fracture_legend = 11 # indegral of c*porosity in the fracture
id_outflux = 2       # integrated outflux across the outflow boundary
id_outflux_legend = 12       # integrated outflux across the outflow boundary

def plot_over_time(file_name, legend, ref, ID, title, ax, lineStyle='-', clr='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 4
    data = np.genfromtxt(file_name, delimiter=",", converters=dict(zip(range(N), [c]*N)))

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    ax.plot(data[:, 0]/(365*24*3600), data[:, ID+1], label=legend, linestyle=lineStyle, color=clr)
    ax.set_xlabel( styles.getTimeLabel('y') )
    ax.grid(True)
    if kwargs.get("has_title", True):
        ax.set_title(title)
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))
    if kwargs.get("xlim", None):
        plt.xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        plt.ylim(kwargs.get("ylim"))

    # choose y-label depending on plot id
    if ID == id_intc_matrix:
        ax.set_ylabel("$\int_{\Omega_3} \phi_3 \, c_3$")
    elif ID == id_intc_fracture:
        ax.set_ylabel("$\int_{\Omega_2} \phi_2 \, c_2$")
    elif ID == id_outflux:
        ax.set_ylabel("outflux")
    else:
        print("Error. Invalid plot id provided.")
        sys.exit(1)

def plot_mean_and_std_over_time(mean_filename, std_filename, legend, ref, ID, title, ax, lineStyle='-', clr='C0', **kwargs):
    c = lambda s: float(s.decode().replace('D', 'e'))
    N = 4

    # Read the mean and standard deviation data
    mean_data = np.genfromtxt(mean_filename, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c]*N)))
    std_data = np.genfromtxt(std_filename, delimiter=",", skip_header=1, converters=dict(zip(range(N), [c]*N)))

    ax.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)

    time = mean_data[:, 0] / (365 * 24 * 3600)
    mean_values = mean_data[:, ID + 1]
    std_values = std_data[:, ID + 1]

    # Plot the mean with a shaded region for the standard deviation
    ax.fill_between(time, mean_values - std_values, mean_values + std_values, color=clr, alpha=0.3)
    ax.plot(time, mean_values, label=legend, linestyle=lineStyle, color=clr)
    
    ax.set_xlabel(styles.getTimeLabel('y'))
    ax.grid(True)

    if kwargs.get("has_title", True):
        ax.set_title(title)
    if kwargs.get("has_legend", True):
        ax.legend(bbox_to_anchor=(1.0, 1.0))
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
        print("Error. Invalid plot id provided.")
        sys.exit(1)

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
            base_dir = os.getcwd().replace("scripts", "results")
            folder = os.path.join(base_dir, place, method)
            datafile = os.path.join(folder, f"dol_refinement_{ref}.csv").replace("\_", "_")

            data = np.genfromtxt(datafile, delimiter=",", converters=dict(zip(range(N), [c] * N)))

            # only take the interesting columns and eleminate nan rows
            data = data[:, 2*ID:2*ID+2];
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

    # choose y-label depending on plot id
    if ID == id_p_matrix:
        ax.set_ylabel( styles.getHeadLabel(3) )
    elif ID == id_c_matrix:
        ax.set_ylabel( styles.getConcentrationLabel(3) )
    elif ID == id_c_fracture:
        ax.set_ylabel( styles.getConcentrationLabel(2) )
    else:
        print("Error. Invalid plot id provided.")
        sys.exit(1)

    return (ls, lowerpercentile, upperpercentile)

