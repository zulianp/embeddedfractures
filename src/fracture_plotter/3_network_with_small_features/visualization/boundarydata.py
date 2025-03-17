import csv
import os

import numpy as np
import plotroutines as plot


def run_boundary_data(places_and_methods={"USI": ["FEM\_LM"], "mean": ["key"]}):
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    results_dir = curr_dir.replace("scripts", "results")
    case = os.path.basename(curr_dir)

    all_data, methods, colors, linestyles = [], [], [], []
    csv_file = f"{curr_dir}_boundary_data_table.csv"
    with open(csv_file, "w", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=",")
        writer.writerow(
            [
                "Method",
                "Outflow 30k",
                "Outflow 150k",
                "Out0/Out 30k",
                "Out0/Out 150k",
                "Inflow 30k",
                "Inflow 150k",
            ]
        )
        for place, meth_list in places_and_methods.items():
            for method in meth_list:
                folder = os.path.join(results_dir, place, method)
                file_name = os.path.join(folder, "results.csv").replace(r"\_", "_")
                label = place if place == "mean" else f"{place}-{method}"
                d = np.genfromtxt(file_name, delimiter=",")
                out = np.sum(d[:2, 6:8], axis=1)
                data = [
                    out[0],
                    out[1],
                    d[0, 6] / out[0],
                    d[1, 6] / out[1],
                    d[0, 8],
                    d[1, 8],
                ]
                writer.writerow([label] + [f"{x:.3f}" for x in data])
                all_data.append(data)
                methods.append(method)
                colors.append(plot.color[place][method])
                linestyles.append(plot.linestyle[place][method])

        # Process reference data
        ref_folder = os.path.join(results_dir, "USTUTT", "MPFA")
        file_name = os.path.join(ref_folder, "results.csv").replace(r"\_", "_")
        d = np.genfromtxt(file_name, delimiter=",")
        ref_ind = 5
        out_val = np.sum(d[ref_ind, 6:8])
        data_ref = [out_val, d[ref_ind, 6] / out_val, d[ref_ind, 8]]
        all_data = np.array(all_data)
        stdvs = np.std(all_data, axis=0)
        writer.writerow(
            [
                "Reference",
                "-",
                f"{data_ref[0]:.3f}",
                "-",
                f"{data_ref[1]:.3f}",
                "-",
                f"{data_ref[2]:.3f}",
            ]
        )
        writer.writerow(
            [
                "Standard deviation",
                f"{stdvs[0]:.3f}",
                f"{stdvs[1]:.3f}",
                "-",
                "-",
                f"{stdvs[4]:.3f}",
                f"{stdvs[5]:.3f}",
            ]
        )
        plot.plot_boundary_data(all_data, methods, data_ref, colors, linestyles)

    # Plot legends for each method
    ncol = 4
    id_legend = 0
    ind = 0
    for place, meth_list in places_and_methods.items():
        for method in meth_list:
            label = place if place == "mean" else f"{place}-{method}"
            plot.plot_legend(
                label,
                id_legend,
                plot.linestyle[place][method],
                plot.color[place][method],
                ncol,
            )
            ind += 1

    plot.save(id_legend, f"{case}_bar_legend")
    plot.crop_pdf(f"{case}_bar_legend")


if __name__ == "__main__":
    run_boundary_data()
