# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d


from fracture_plotter.utils.plot_routines_utils import *


def plot_over_line(
    filename, label, ref, title, ax, linestyle="-", color="C0", fontsize=30, **kwargs
):
    N = 2
    load_args = make_load_args(filename, N)
    plot_args = make_plot_args(label, linestyle=linestyle, color=color)

    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)
        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, 0],
            mean_values=mean_data[:, 1],
            std_values=std_data[:, 1],
            **plot_args,
        )

    else:
        data = load_data(**load_args, skip_header=0)
        ax.plot(data[:, 0], data[:, 1], **plot_args)

    format_axis(
        ax,
        ref,
        fontsize,
        xlabel=styles.getArcLengthLabel(),
        ylabel=styles.getHeadLabel(3),
        title=title if kwargs.get("show_title", False) else None,
        show_legend=kwargs.get("show_legend", False),
        xlim=kwargs.get("xlim", None),
        ylim=kwargs.get("ylim", None),
    )


def plot_over_time(
    filename,
    label,
    title,
    region,
    region_pos,
    ax,
    linestyle="-",
    color="C0",
    fontsize=30,
    **kwargs
):
    # Get the number of columns
    N = min(22, len(np.genfromtxt(filename, delimiter=",", max_rows=1, skip_header=1)))
    load_args = make_load_args(filename, N)
    plot_args = make_plot_args(label, linestyle=linestyle, color=color)

    region_idx = region + 1

    if "mean" in filename:
        mean_data, std_data = load_mean_and_std_data(**load_args, skip_header=1)
        plot_mean_and_std_data(
            ax=ax,
            x=mean_data[:, 0],
            mean_values=mean_data[:, region_idx],
            std_values=std_data[:, region_idx],
            **plot_args,
        )
    else:
        data = load_data(**load_args, skip_header=0)
        if "/USI/" in filename:
            if region == 1:
                region_idx = 1
            elif region == 10:
                region_idx = 2
            elif region == 11:
                region_idx = 3

        ax.plot(data[:, 0], data[:, region_idx], **plot_args)

    format_axis(
        ax,
        region_pos,
        fontsize,
        xlabe=styles.getTimeLabel(),
        ylabel=styles.getConcentrationLabel(3),
        title=title if kwargs.get("show_title", False) else None,
        show_legend=kwargs.get("show_legend", False),
        xlim=kwargs.get("xlim", None),
        ylim=kwargs.get("ylim", None),
    )
