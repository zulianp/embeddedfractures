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

# places_and_methods = {
#     "USI": ["FEM\_LM"],
#     "mean": ["key"],
# }

# Plot IDs (case 1)
id_p_matrix, id_c_matrix, id_c_fracture = 0, 1, 2
id_intc_matrix, id_intc_fracture, id_outflux = 0, 1, 2

# Plot IDs (case 3 + 4)
id_p_0_matrix, id_p_0_matrix_legend = 0, 10
id_p_1_matrix, id_p_1_matrix_legend = 1, 11  # p along (0, 100, 100)-(100, 0, 0)

# Plot IDs (case 3 + 4)
id_pot, id_pot_legend = 2, 12


def make_load_args(filename, n_columns):
    converters = {i: decode_float for i in range(n_columns)}
    return {"filename": filename, "n_columns": n_columns, "converters": converters}


def make_plot_args(label, linestyle="-", color="C0"):
    return {"label": label, "linestyle": linestyle, "color": color}


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

    if "xticks" in kwargs:
        ax.set_xticks(kwargs["xticks"])
    if "yticks" in kwargs:
        ax.set_yticks(kwargs["yticks"])


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
def decode_float(s):
    return float(s.decode().replace("D", "e"))


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


def make_extra_args(kwargs):
    extra_args = {}

    xlim = kwargs.get("xlim", None)
    ylim = kwargs.get("ylim", None)
    xticks = kwargs.get("xticks", None)
    yticks = kwargs.get("yticks", None)

    if xlim is not None:
        extra_args["xlim"] = xlim
    if ylim is not None:
        extra_args["ylim"] = ylim
    if xticks is not None:
        extra_args["xticks"] = xticks
    if yticks is not None:
        extra_args["yticks"] = yticks

    return extra_args


def plot_over_line_helper(
    filename, ax, data_idx, num_columns, label, linestyle, color, **kwargs
):
    load_args = make_load_args(filename, num_columns)
    plot_args = make_plot_args(label, linestyle=linestyle, color=color)

    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)
        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, data_idx],
            mean_values=mean_data[:, data_idx + 1],
            std_values=std_data[:, data_idx + 1],
            **plot_args,
        )
    else:
        data = load_data(**load_args, skip_header=0)
        ax.plot(data[:, data_idx], data[:, data_idx + 1], **plot_args)

    extra_format_args = make_extra_args(kwargs)

    format_axis(
        ax=ax,
        ref=kwargs.get("ref", 0),
        fontsize=kwargs.get("fontsize", 30),
        xlabel=kwargs.get("xlabel", None),
        ylabel=kwargs.get("ylabel", None),
        title=kwargs.get("title", None),
        show_legend=kwargs.get("show_legend", False),
        **extra_format_args,
    )


def plot_over_line(
    case,
    filename,
    label,
    title,
    ax,
    ref=None,
    ID=None,
    linestyle="-",
    color="C0",
    fontsize=30,
    **kwargs,
):
    if case == 1:
        if ref is None or ID is None:
            raise ValueError("Case 1 requires both ref and ID.")
        num_columns, data_idx = 5, 2 * ID
        ylabel = {
            id_p_matrix: styles.getHeadLabel(3),
            id_c_matrix: styles.getConcentrationLabel(3),
            id_c_fracture: styles.getConcentrationLabel(2),
        }.get(ID)
        plot_over_line_helper(
            filename=filename,
            ax=ax,
            data_idx=data_idx,
            num_columns=num_columns,
            label=label,
            linestyle=linestyle,
            color=color,
            ref=ref,
            fontsize=fontsize,
            xlabel=styles.getArcLengthLabel(),
            ylabel=ylabel,
            title=title,
            xlim=kwargs.get("xlim"),
            ylim=kwargs.get("ylim"),
            **kwargs,
        )
    elif case in (2, 3):
        if ref is None:
            raise ValueError("Case 2 and 3 require ref.")
        num_columns, data_idx = 2, 0
        plot_over_line_helper(
            filename=filename,
            ax=ax,
            data_idx=data_idx,
            num_columns=num_columns,
            label=label,
            linestyle=linestyle,
            color=color,
            ref=ref,
            fontsize=fontsize,
            xlabel=styles.getArcLengthLabel(),
            ylabel=styles.getHeadLabel(3),
            title=title,
            xlim=kwargs.get("xlim"),
            ylim=kwargs.get("ylim"),
            **kwargs,
        )
    elif case == 4:
        if ID is None:
            raise ValueError("Case 4 requires ID.")
        num_columns, data_idx = 2, 0
        extra_params = {}
        if ID == id_p_0_matrix:
            extra_params = {
                "xticks": [0, 500, 1000, 1500],
                "yticks": [0, 100, 200, 300, 400, 500, 600, 700],
            }
        elif ID == id_p_1_matrix:
            extra_params = {
                "xticks": [0, 500, 1000, 1500],
                "yticks": [0, 50, 100, 150, 200, 250],
            }
        plot_over_line_helper(
            filename=filename,
            ax=ax,
            data_idx=data_idx,
            num_columns=num_columns,
            label=label,
            linestyle=linestyle,
            color=color,
            fontsize=fontsize,
            xlabel=styles.getArcLengthLabel(),
            ylabel=styles.getHeadLabel(3),
            title=title,
            xlim=kwargs.get("xlim"),
            ylim=kwargs.get("ylim"),
            **extra_params,
            **kwargs,
        )

    else:
        raise ValueError(f"Unknown case number: {case}")


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
