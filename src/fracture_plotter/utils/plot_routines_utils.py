import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

places_and_methods = {
    "USI": ["FEM\_LM"],
    "mean": ["key"],
}


# class MathTextSciFormatter(mticker.Formatter):
#     def __init__(self, fmt="%1.2e"):
#         self.fmt = fmt
#     def __call__(self, x, pos=None):
#         s = self.fmt % x
#         decimal_point = '.'
#         positive_sign = '+'
#         tup = s.split('e')
#         significand = tup[0].rstrip(decimal_point)
#         sign = tup[1][0].replace(positive_sign, '')
#         exponent = tup[1][1:].lstrip('0')
#         if exponent:
#             exponent = '10^{%s%s}' % (sign, exponent)
#         if significand and exponent:
#             s =  r'%s{\times}%s' % (significand, exponent)
#         else:
#             s =  r'%s%s' % (significand, exponent)
#         return "${}$".format(s)
class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2f"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        return "${}$".format(s)


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=1):
    # it looks like that figure_ID = 1 gives problems, so we add a random number = 11
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol)


def save(ID, filename, extension=".pdf", plots_dir=None, **kwargs):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    fig = plt.figure(ID + 11)

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
            )

    plt.savefig(os.path.join(plots_dir, filename + extension), bbox_inches="tight")
    plt.gcf().clear()


def crop_pdf(filename, plots_dir):
    filename = os.path.join(plots_dir, f"{filename}.pdf")
    if os.path.isfile(filename):
        os.system("pdfcrop --margins '0 -300 0 0' " + filename + " " + filename)
        os.system("pdfcrop " + filename + " " + filename)
