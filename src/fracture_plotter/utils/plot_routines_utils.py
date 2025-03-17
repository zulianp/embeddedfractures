from __future__ import print_function

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# plot_utils.py
import numpy as np
from scipy import integrate, interpolate

import fracture_plotter.utils.styles as styles

os.environ["PATH"] += ":/Library/TeX/texbin"
plt.rc("text", usetex=True)
plt.rc("font", family="serif")

plt.rc("text", usetex=True)
plt.rc("font", family="serif")
plt.rc("font", size=15)

linestyle = styles.linestyle
color = styles.color

places_and_methods = {
    "USI": ["FEM\_LM"],
    "mean": ["key"],
}


def format_axis(ax, ref, fontsize, **kwargs):
    ax.grid(True)
    ax.tick_params(axis="x", labelsize=fontsize)
    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)
    else:
        formatter = mticker.ScalarFormatter(useMathText=True)
        formatter.set_powerlimits((-2, 2))
        ax.yaxis.set_major_formatter(formatter)
        ax.yaxis.get_offset_text().set_fontsize(fontsize)
        ax.yaxis.get_offset_text().set_visible(True)
        ax.yaxis.set_tick_params(labelsize=fontsize)

    xlabel = kwargs.get("xlabel", None)
    ylabel = kwargs.get("ylabel", None)
    title = kwargs.get("title", None)
    show_legend = kwargs.get("show_legend", False)

    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)
    if show_legend:
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)

    if "xlim" in kwargs:
        ax.set_xlim(kwargs["xlim"])
    if "ylim" in kwargs:
        ax.set_ylim(kwargs["ylim"])


class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2f"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        return "${}$".format(s)


def setup_figure(id_offset, num_axes, xlim=None, ylim=None):
    fig, axes_list = plt.subplots(
        1, num_axes, figsize=(16, 8), sharex=True, sharey=True, num=id_offset + 11
    )
    fig.subplots_adjust(hspace=0.4, wspace=0)

    if xlim is not None:
        for ax in axes_list:
            ax.set_xlim(xlim)

    if ylim is not None:
        for ax in axes_list:
            ax.set_ylim(ylim)

    return fig, axes_list


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1, fontsize=30):
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol, fontsize=fontsize)


def save(ID, filename, extension=".pdf", plots_dir=None, fontsize=30, **kwargs):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    fig = plt.figure(ID + 11)
    ax_title = kwargs.get("ax_title", None)

    for idx, ax in enumerate(fig.get_axes()):
        ax.label_outer()
        if len(fig.get_axes()) > 1:
            index = 97 + idx + kwargs.get("starting_from", 0)
            text = "\\textbf{subfig. " + chr(index) + "}"
            ax.text(
                0.5,
                -0.2,
                text,
                horizontalalignment="center",
                verticalalignment="bottom",
                transform=ax.transAxes,
                fontsize=fontsize,
            )
        elif ax_title is not None:
            print("asd")
            ax.text(
                0.5,
                -0.25,
                ax_title,
                horizontalalignment="center",
                verticalalignment="bottom",
                transform=ax.transAxes,
            )

    plt.savefig(os.path.join(plots_dir, filename + extension), bbox_inches="tight")
    plt.gcf().clear()


def crop_pdf(filename, plots_dir):
    filename = os.path.join(plots_dir, f"{filename}.pdf")
    if os.path.isfile(filename):
        os.system("pdfcrop --margins '0 -300 0 0' " + filename + " " + filename)
        os.system("pdfcrop " + filename + " " + filename)


################## SUGGESTED COMMON FUNCTIONALITY ##################
def load_data(filename, n_columns, converters=None, skip_header=0):
    """Load data from a CSV file with optional converters."""
    if converters is None:
        converters = {
            i: lambda s: float(s.decode().replace("D", "e")) for i in range(n_columns)
        }
    return np.genfromtxt(
        filename, delimiter=",", skip_header=skip_header, converters=converters
    )


def load_mean_and_std_data(filename, n_columns, converters, skip_header=1):
    """Load mean and standard deviation data from CSV files."""
    mean_data = load_data(
        filename=filename,
        n_columns=n_columns,
        converters=converters,
        skip_header=skip_header,
    )
    std_data = load_data(
        filename=filename.replace("mean", "std"),
        n_columns=n_columns,
        converters=converters,
        skip_header=skip_header,
    )
    if mean_data.shape != std_data.shape:
        raise ValueError("Mean and standard deviation data do not have the same shape!")

    return mean_data, std_data


def plot_mean_and_std_data(ax, x, mean_values, std_values, **kwargs):
    color = kwargs.get("color", "C0")
    alpha = kwargs.get("alpha", 0.5)
    label = kwargs.get("label", None)
    linestyle = kwargs.get("linestyle", "-")

    ax.fill_between(
        x, mean_values - std_values, mean_values + std_values, color=color, alpha=alpha
    )
    ax.plot(x, mean_values, label=label, linestyle=linestyle, color=color)

    xlim = kwargs.get("xlim", None)
    ylim = kwargs.get("ylim", None)
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)


def plot_legend_in_middle(**kwargs):
    # One axis case
    ax = kwargs.get("ax", None)
    fontsize = kwargs.get("fontsize", 30)

    if ax is not None:
        handles, labels = ax.get_legend_handles_labels()

        if isinstance(ax, (list, np.ndarray)):  # Check if it's an array of subplots
            mid_ax = ax[len(ax) // 2]  # Select the middle axis for the legend
            mid_ax.legend(
                handles,
                labels,
                loc="upper center",
                bbox_to_anchor=(0.5, -0.2),
                ncol=4,
                fontsize=fontsize,
            )
        else:  # Single plot
            ax.legend(
                handles,
                labels,
                loc="upper center",
                bbox_to_anchor=(0.5, -0.3),
                ncol=2,
                fontsize=fontsize,
            )

    if ax is None:
        fig = kwargs.get("fig", None)
        ax1 = kwargs.get("ax1", None)
        ax2 = kwargs.get("ax2", None)

        if fig is None or ax1 is None or ax2 is None:
            raise ValueError("Either ax or fig and ax1 and ax2 must be provided!")
        else:
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
                fontsize=fontsize,
            )
