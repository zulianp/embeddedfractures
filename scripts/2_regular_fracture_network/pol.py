import os
import plotroutines as plot


def plot_data_over_lines(places_and_methods, results_dir, ref, ax, title, cond, show_legend=False, fmt="%1.2e"):
    for place in places_and_methods:
        for method in places_and_methods[place]:
            folder = os.path.join(results_dir, place, method).replace("\_", "_")
            data = os.path.join(folder, f"dol_cond_{cond}_refinement_{ref}.csv").replace("\_", "_")
            label = place + ("-" + method if place.replace("\_", "_") != "mean" else "")
            plot.plot_over_line(data, label, ref, title, cond, ax,
                                plot.linestyle[place][method], plot.color[place][method],
                                has_legend=show_legend, fmt=fmt)

    # Add reference (4th refinement of USTUTT-MPFA)
    ref_data = os.path.join(results_dir, f"USTUTT/MPFA/dol_cond_{cond}_refinement_4.csv".replace("\_", "_"))
    plot.plot_over_line(ref_data, "reference", ref, title, cond, ax,
                        plot.linestyle["USTUTT"]["reference"], plot.color["USTUTT"]["reference"],
                        has_legend=show_legend, fmt=fmt)


def run_pol(places_and_methods={"USTUTT": ["MPFA"], "mean": ["key"]}):
    # Get directories
    curr_dir, plots_dir, results_dir, _ = plot.get_paths()
    case = curr_dir.split(os.sep)[-1]  # case we are dealing with
    titles = ['$\\sim 500$ cells', '$\\sim 4k$ cells', '$\\sim 32k$ cells']
    refinement_index = [0, 1, 2]
    conds = [0]  # Add other conditions if needed

    ylim_dict = {0: (0.5, 2.75), 1: (0.4, 5.75)}
    fmt_dict = {0: "%1.2f", 1: "%1.2e"}

    for cond in conds:
        fig, axes_list = plot.setup_figure(cond, 3, ylim_dict.get(cond))

        for title, ref, idx, ax in zip(titles, refinement_index, range(3), axes_list):
            show_legend = (idx == 1)  # Show legend only for middle subplot
            fmt = fmt_dict.get(cond)

            plot_data_over_lines(places_and_methods, results_dir, ref, ax, title, cond, show_legend, fmt)

            if idx == 1:
                plot.plot_legend_in_middle(ax)  # Only add legend to middle subplot

        # Save the figure
        plot.save(ID=cond, filename=f"{case}_pol_cond_{cond}")

    # Optionally add cropped legend
    plot.crop_pdf(f"{case}_pol_cond_{cond}_legend")


if __name__ == "__main__":
    run_pol()
