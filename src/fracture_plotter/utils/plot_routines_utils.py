from __future__ import print_function

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

os.environ["PATH"] += ":/Library/TeX/texbin"
plt.rc("text", usetex=True)
plt.rc("font", family="serif")

import os

import numpy as np

import fracture_plotter.utils.styles as styles

plt.rc("text", usetex=True)
plt.rc("font", family="serif")
plt.rc("font", size=15)

linestyle = styles.linestyle
color = styles.color

places_and_methods = {
    "USI": ["FEM\_LM"],
    "mean": ["key"],
}


class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2f"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        return "${}$".format(s)


# def setup_figure(id_offset, num_axes, ylim):
#     fig = plt.figure(
#         id_offset + 11, figsize=(16, 8)
#     )  # Increased figure height to accommodate the legend
#     fig.subplots_adjust(hspace=0.4, wspace=0)  # Increase space between plots vertically
#     axes_list = [
#         fig.add_subplot(1, num_axes, idx + 1, ylim=ylim) for idx in range(num_axes)
#     ]
#     return fig, axes_list


def setup_figure(id_offset, num_axes, ylim):
    fig, axes_list = plt.subplots(
        1, num_axes, figsize=(16, 8), sharex=True, sharey=True, num=id_offset + 11
    )
    fig.subplots_adjust(hspace=0.4, wspace=0)

    # Apply ylim to all subplots
    for ax in axes_list:
        ax.set_ylim(ylim)

    return fig, axes_list


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1):
    # It looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol)


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
