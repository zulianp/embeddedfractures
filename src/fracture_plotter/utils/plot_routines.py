from __future__ import print_function

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from scipy import interpolate
from scipy.integrate import simpson as simps

import fracture_plotter.utils.styles as styles
from fracture_plotter.utils.general import get_paths

os.environ["PATH"] += ":/Library/TeX/texbin"
plt.rc("text", usetex=True)
plt.rc("font", family="serif")

linestyle = styles.linestyle
color = styles.color

fontsize = 30
subfig_fontsize = 25
ncol = 4  # for the legend in plots

# Plot IDs (case 1)
id_p_matrix, id_c_matrix, id_c_fracture = 0, 1, 2
id_intc_matrix, id_intc_fracture, id_outflux = 0, 1, 2

# Plot IDs (cases 3 & 4)
id_p_0_matrix, id_p_0_matrix_legend = 0, 10
id_p_1_matrix, id_p_1_matrix_legend = 1, 11
id_pot, id_pot_legend = 2, 12


class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2f"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        return "${}$".format(s)


def get_places_and_methods_arg(places_and_methods, ref):
    return (
        places_and_methods[ref]
        if isinstance(places_and_methods, dict)
        else places_and_methods
    )


def decode_float(s):
    return float(s.replace("D", "e"))


def load_data(filename, n_columns, converters=None, skip_header=0):
    converters = converters or {i: decode_float for i in range(n_columns)}
    return np.genfromtxt(
        filename, delimiter=",", skip_header=skip_header, converters=converters
    )


def load_mean_and_std_data(filename, n_columns, converters, skip_header=1):
    mean_data = load_data(filename, n_columns, converters, skip_header)
    std_data = load_data(
        filename.replace("mean", "std"), n_columns, converters, skip_header
    )
    if mean_data.shape != std_data.shape:
        raise ValueError("Mean and standard deviation data do not have the same shape!")
    return mean_data, std_data


def make_load_args(filename, n_columns):
    return {
        "filename": filename,
        "n_columns": n_columns,
        "converters": {i: decode_float for i in range(n_columns)},
    }


def make_plot_args(label, linestyle="-", color="C0"):
    return {"label": label, "linestyle": linestyle, "color": color}


def make_extra_args(kwargs):
    return {k: kwargs[k] for k in ("xlim", "ylim", "xticks", "yticks") if k in kwargs}


def format_axis(ax, ref, fontsize, **kwargs):
    ax.grid(True)
    ax.tick_params(axis="x", labelsize=fontsize)
    if int(ref) > 0:
        ax.yaxis.set_tick_params(length=0)
    else:
        fmt = mticker.ScalarFormatter(useMathText=True)
        fmt.set_powerlimits((-2, 2))
        ax.yaxis.set_major_formatter(fmt)
        ax.yaxis.get_offset_text().set_fontsize(fontsize)
        ax.yaxis.get_offset_text().set_visible(True)
        ax.yaxis.set_tick_params(labelsize=fontsize)

    ax.set_xlabel(kwargs.get("xlabel"), fontsize=fontsize)
    ax.set_ylabel(kwargs.get("ylabel"), fontsize=fontsize)
    ax.set_title(kwargs.get("title"), fontsize=fontsize)

    if kwargs.get("show_legend", False):
        ax.legend(bbox_to_anchor=(1.0, 1.0), fontsize=fontsize)
    if "xlim" in kwargs:
        ax.set_xlim(kwargs["xlim"])
    if "ylim" in kwargs:
        ax.set_ylim(kwargs["ylim"])
    if "xticks" in kwargs:
        ax.set_xticks(kwargs["xticks"])
    if "yticks" in kwargs:
        ax.set_yticks(kwargs["yticks"])


def setup_figure(id_offset, num_axes, xlim=None, ylim=None):
    fig, axes_list = plt.subplots(
        1, num_axes, figsize=(16, 8), sharex=True, sharey=True, num=id_offset + 11
    )
    fig.subplots_adjust(hspace=0.4, wspace=0)
    for ax in axes_list:
        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)
    return fig, axes_list


def plot_legend(legend, ID, linestyle="-", color="C0", ncol=ncol, fontsize=30):
    plt.figure(ID + 11)
    plt.plot(np.zeros(1), label=legend, linestyle=linestyle, color=color)
    plt.legend(bbox_to_anchor=(1, -0.2), ncol=ncol, fontsize=fontsize)


def plot_legend_in_middle(**kwargs):
    ax = kwargs.get("ax")
    fontsize = kwargs.get("fontsize", 30)
    if ax is not None:
        handles, labels = ax.get_legend_handles_labels()
        if isinstance(ax, (list, np.ndarray)):
            ax[len(ax) // 2].legend(
                handles,
                labels,
                loc="upper center",
                bbox_to_anchor=(0.5, -0.3),
                ncol=ncol,
                fontsize=fontsize,
            )
        else:
            ax.legend(
                handles,
                labels,
                loc="upper center",
                bbox_to_anchor=(0.5, -0.3),
                ncol=ncol,
                fontsize=fontsize,
            )
    else:
        fig, ax1, ax2 = kwargs.get("fig"), kwargs.get("ax1"), kwargs.get("ax2")
        if not all([fig, ax1, ax2]):
            raise ValueError("Either ax or fig and ax1 and ax2 must be provided!")
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        unique_handles, unique_labels = [], []
        for h, l in zip(handles1 + handles2, labels1 + labels2):
            if l not in unique_labels:
                unique_handles.append(h)
                unique_labels.append(l)
        fig.legend(
            unique_handles,
            unique_labels,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.1),
            ncol=ncol,
            fontsize=fontsize,
        )


def save(ID, filename, extension=".pdf", plots_dir=None, fontsize=30, **kwargs):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    fig = plt.figure(ID + 11)
    ax_title = kwargs.get("ax_title")
    for idx, ax in enumerate(fig.get_axes()):
        ax.label_outer()
        if len(fig.get_axes()) > 1:
            index = 97 + idx + kwargs.get("starting_from", 0)
            ax.text(
                0.5,
                -0.2,
                f"\\textbf{{subfig. {chr(index)}}}",
                horizontalalignment="center",
                verticalalignment="bottom",
                transform=ax.transAxes,
                fontsize=fontsize,
            )
        elif ax_title is not None:
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
    filepath = os.path.join(plots_dir, f"{filename}.pdf")
    if os.path.isfile(filepath):
        os.system(f"pdfcrop --margins '0 -300 0 0' {filepath} {filepath}")
        os.system(f"pdfcrop {filepath} {filepath}")


def plot_mean_and_std_data(ax, x, mean_values, std_values, **kwargs):
    color = kwargs.get("color", "C0")
    ax.fill_between(
        x,
        mean_values - std_values,
        mean_values + std_values,
        color=color,
        alpha=kwargs.get("alpha", 0.5),
    )
    ax.plot(
        x,
        mean_values,
        label=kwargs.get("label"),
        linestyle=kwargs.get("linestyle", "-"),
        color=color,
    )
    if kwargs.get("xlim") is not None:
        ax.set_xlim(kwargs["xlim"])
    if kwargs.get("ylim") is not None:
        ax.set_ylim(kwargs["ylim"])


def plot_helper(
    filename, ax, x_idx, y_idx, num_columns, label, linestyle, color, **kwargs
):
    load_args = make_load_args(filename, num_columns)
    plot_args = make_plot_args(label, linestyle=linestyle, color=color)
    x_transform = kwargs.get("x_transform", 1.0)

    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)
        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, x_idx] * x_transform,
            mean_values=mean_data[:, y_idx],
            std_values=std_data[:, y_idx],
            **plot_args,
        )
    else:
        data = load_data(**load_args, skip_header=0)
        ax.plot(data[:, x_idx] * x_transform, data[:, y_idx], **plot_args)

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
    params = dict(
        filename=filename,
        ax=ax,
        label=label,
        linestyle=linestyle,
        color=color,
        fontsize=fontsize,
        xlabel=styles.getArcLengthLabel(),
        title=title,
        xlim=kwargs.get("xlim"),
        ylim=kwargs.get("ylim"),
        num_columns=2,
        x_idx=0,
        y_idx=1,
    )

    if case == "single_fracture":
        if ref is None or ID is None:
            raise ValueError("Case single_fracture requires both ref and ID.")
        params.update(
            ref=ref,
            num_columns=5,
            x_idx=2 * ID,
            y_idx=2 * ID + 1,
            ylabel={
                id_p_matrix: styles.getHeadLabel(3),
                id_c_matrix: styles.getConcentrationLabel(3),
                id_c_fracture: styles.getConcentrationLabel(2),
            }.get(ID),
        )
    elif case in ("regular_fracture", "small_features"):
        if ref is None:
            raise ValueError("Case regular_fracture and small_features require ref.")
        params.update(ref=ref, ylabel=styles.getHeadLabel(3))
    elif case == "field_case":
        if ID is None:
            raise ValueError("Case field_case requires ID.")
        params["ylabel"] = styles.getHeadLabel(3)
        if ID == id_p_0_matrix:
            params.update(
                xticks=[0, 500, 1000, 1500],
                yticks=[0, 100, 200, 300, 400, 500, 600, 700],
            )
        elif ID == id_p_1_matrix:
            params.update(
                xticks=[0, 500, 1000, 1500],
                yticks=[0, 50, 100, 150, 200, 250],
            )
    else:
        raise ValueError(f"Unknown case number: {case}")

    params.update(kwargs)
    plot_helper(**params)


def plot_over_time(
    case,
    filename,
    label,
    title,
    ax,
    ref=None,
    ID=None,
    region=None,
    region_pos=None,
    linestyle="-",
    color="C0",
    fontsize=30,
    **kwargs,
):
    params = dict(
        filename=filename,
        ax=ax,
        label=label,
        title=title,
        linestyle=linestyle,
        color=color,
        fontsize=fontsize,
        xlim=kwargs.get("xlim"),
        ylim=kwargs.get("ylim"),
        x_idx=0,
        y_idx=1,
        xlabel=styles.getTimeLabel("s"),
    )

    if case == "single_fracture":
        if ref is None or ID is None:
            raise ValueError("Case single_fracture requires both ref and ID.")
        params.update(
            ref=ref,
            num_columns=4,
            x_idx=ID,
            y_idx=ID + 1,
            xlabel=styles.getTimeLabel("y"),
            ylabel={
                id_intc_matrix: r"$\int_{\Omega_3} \phi_3 \, c_3$",
                id_intc_fracture: r"$\int_{\Omega_2} \phi_2 \, c_2$",
                id_outflux: "outflux",
            }.get(ID),
            x_transform=1 / (365 * 24 * 3600),
        )
    elif case == "regular_fracture":
        if region is None or region_pos is None:
            raise ValueError(
                "Case regular_fracture requires both region and region_pos."
            )
        num_cols = min(
            22, len(np.genfromtxt(filename, delimiter=",", max_rows=1, skip_header=1))
        )

        y_idx = region + 1
        if "mean" not in filename and "/USI/" in filename:
            if region == 1:
                y_idx = 1
            elif region == 10:
                y_idx = 2
            elif region == 11:
                y_idx = 3

        params.update(
            num_columns=num_cols,
            region=region,
            region_pos=region_pos,
            y_idx=y_idx,
            ylabel=styles.getConcentrationLabel(3),
        )
    elif case == "small_features":
        if ref is None or ID is None:
            raise ValueError("Case small_features requires both ref and ID.")
        params.update(
            ref=ref,
            num_columns=9,
            x_idx=0,
            y_idx=ID + 1,
            ylabel=r"$\overline{c_2}$",
        )
    elif case == "field_case":
        if region is None or region_pos is None:
            raise ValueError("Case field_case requires both region and region_pos.")
        params.update(
            num_columns=53,
            region=region,
            region_pos=region_pos,
            y_idx=region + 1,
            ylabel=styles.getAveragedConcentrationLabel(2),
            xticks=[0, 500, 1000, 1500],
        )
    else:
        raise ValueError(f"Unknown case number: {case}")

    params.update(kwargs)
    plot_helper(**params)


def plot_percentiles(
    case,
    paths,
    places_and_methods,
    ax,
    ref=None,
    ID=None,
    line_id=None,
    cond=None,
    fontsize=30,
    **kwargs,
):
    params = dict(
        ax=ax,
        fontsize=fontsize,
        ylim=kwargs.get("ylim"),
        col_indices=slice(0, 2),
        num_columns=2,
        xlabel=styles.getArcLengthLabel(),
        ylabel=styles.getHeadLabel(3),
    )

    if case == "single_fracture":
        if ref is None or ID is None:
            raise ValueError("Case single_fracture requires both ref and ID.")
        ylabel = {
            id_p_matrix: styles.getHeadLabel(3),
            id_c_matrix: styles.getConcentrationLabel(3),
            id_c_fracture: styles.getConcentrationLabel(2),
        }.get(ID)

        params.update(
            num_columns=6,
            ylabel=ylabel,
            col_indices=slice(2 * ID, 2 * ID + 2),
            filename=f"dol_refinement_{ref}.csv",
        )
    elif case == "regular_fracture":
        if cond is None or ref is None:
            raise ValueError("Case regular_fracture requires cond.")
        params.update(filename=f"dol_cond_{cond}_refinement_{ref}.csv")
    elif case == "small_features":
        if ref is None or line_id is None:
            raise ValueError("Case small_features requires both ref and line_id.")
        params.update(filename=f"dol_line_{line_id}_refinement_{ref}.csv")
    elif case == "field_case":
        if ref is None:
            raise ValueError("Case field_case requires ref.")
        y_ticks = (
            [0, 100, 200, 300, 400, 500, 600, 700]
            if ref == "0"
            else [0, 50, 100, 150, 200, 250]
        )
        params.update(
            filename=f"dol_line_{ref}.csv", xticks=[0, 500, 1000, 1500], yticks=y_ticks
        )

    funcs, minX, maxX = [], -np.inf, np.inf
    for place, methods in places_and_methods.items():
        if case == "single_fracture" and place == "DTU" and ID != id_p_matrix:
            continue
        for method in methods:
            datafile = os.path.join(
                paths.results_dir, place, method, params["filename"]
            ).replace("\_", "_")
            data = load_data(datafile, params["num_columns"])
            data = data[:, params["col_indices"]]
            data = data[~np.isnan(data).any(axis=1)]

            funcs.append(interpolate.interp1d(data[:, 0], data[:, 1]))
            minX, maxX = max(minX, data[0, 0]), min(maxX, data[-1, 0])

    ls = np.linspace(minX, maxX, num=1000)
    interpolated = [f(ls) for f in funcs]
    mean_values = np.mean(interpolated, axis=0)
    lower, upper = np.percentile(interpolated, [10, 90], axis=0)

    ax.fill_between(ls, lower, upper, color="gray")
    ax.set_xlabel(params.get("xlabel"), fontsize=fontsize)
    ax.set_ylabel(params.get("ylabel"), fontsize=fontsize)
    weighted_area = (simps(upper, ls) - simps(lower, ls)) / simps(mean_values, ls)
    ax.set_title(f"weighted area {MathTextSciFormatter()(weighted_area)}")
    ax.grid(True)

    if kwargs.get("xlim", None):
        ax.set_xlim(kwargs.get("xlim"))
    if kwargs.get("ylim", None):
        ax.set_ylim(kwargs.get("ylim"))
    if params.get("xticks", None):
        ax.set_xticks(params.get("xticks"))
    if params.get("yticks", None):
        ax.set_yticks(params.get("yticks"))

    return ls, lower, upper


### Case small_features only ###
def save_over_time(filename, extension=".pdf", plots_dir=None, fontsize=25):
    for ID in np.arange(8):
        save(
            ID=ID,
            filename=f"{filename}_fracture_{ID}",
            extension=extension,
            plots_dir=plots_dir,
            fontsize=fontsize,
        )


def plot_boundary_data(data, methods, data_ref, colors, linestyle, extension=".pdf"):
    plot_boundary_head(data[:, 4:], methods, data_ref[2], colors, linestyle, extension)
    plot_boundary_fluxes(
        data[:, :4], methods, data_ref[1], colors, linestyle, extension
    )
    plot_reference_fluxes(
        data[:, :4], methods, data_ref[1], colors, linestyle, extension
    )


def plot_boundary_fluxes(da, methods, ratio_ref, colors, linestyle, extension):
    paths = get_paths(__file__)

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
        ax.bar(ind + width * i, da[:, i + 2], width, color=c, edgecolor="white")

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
    os.makedirs(paths.plots_dir, exist_ok=True)

    text = "\\textbf{subfig. b}"
    ax.text(
        0.5,
        -0.2,
        text,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )

    plt.savefig(
        os.path.join(paths.plots_dir, f"{paths.case}_boundary_head" + extension),
        bbox_inches="tight",
    )


def plot_reference_fluxes(da, colors, linestyle, extension):
    paths = get_paths(__file__)

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
    os.makedirs(paths.plots_dir, exist_ok=True)

    text = "\\textbf{subfig. a}"
    ax.text(
        0.5,
        -0.2,
        text,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )

    plt.savefig(
        os.path.join(paths.plots_dir, f"{paths.case}_reference_flux" + extension),
        bbox_inches="tight",
    )


def plot_boundary_head(da, methods, head_ref, colors, linestyle, extension):
    paths = get_paths(__file__)

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
        ax.bar(
            ind + width * i, da[:, i], width, color=c, edgecolor="white"
        )  # , hatch=linestyle)

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

    os.makedirs(paths.plots_dir, exist_ok=True)

    text = "\\textbf{subfig. c}"
    ax.text(
        0.5,
        -0.2,
        text,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax.transAxes,
    )

    plt.savefig(
        os.path.join(paths.plots_dir, f"{paths.case}_boundary_fluxes" + extension),
        bbox_inches="tight",
    )
