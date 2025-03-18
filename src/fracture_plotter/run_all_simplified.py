import json
import os
import pprint

import fracture_plotter.utils.csv as csv_tools
from fracture_plotter.utils.compute_mean_and_std_all import compute_mean_and_std
from fracture_plotter.utils.general import (
    get_focus_institute_and_method,
    get_paths,
    process_args,
)
from fracture_plotter.utils.overlay import run_overlay
from fracture_plotter.utils.plot_routines import fontsize, subfig_fontsize

comp_mean_std = True  # compute the mean and std of the results
methods_mean_std = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]
focus_inst, focus_meth = get_focus_institute_and_method(current=True)

create_pdfs = True  # create plots in PDF format
places_and_methods = {
    focus_inst: [focus_meth],
    "mean": ["key"],
}  # what we choose to plot (std filename is inferred from mean)
case_list = [
    # "single_fracture",
    # "regular_fracture",
    # "small_features",
    "field_case"
]

copy_pdfs_to_overleaf = False  # copy the PDF plots to the overleaf project


def run_all_single_fracture(paths):
    from fracture_plotter.single_fracture.visualization.percentiles import (
        run_percentiles,
    )
    from fracture_plotter.single_fracture.visualization.pol import run_pol
    from fracture_plotter.single_fracture.visualization.pot import run_pot

    run_percentiles(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )

    run_pol(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )
    run_pot(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )

    files = [
        os.path.join(paths.tex_dir, "pol_c_fracture"),
        os.path.join(paths.tex_dir, "pol_c_matrix"),
        os.path.join(paths.tex_dir, "pol_p_matrix"),
        os.path.join(paths.tex_dir, "pot_outflux"),
    ]

    run_overlay(paths, files)


def run_all_regular_fracture(paths):
    from fracture_plotter.regular_fracture.visualization.pol import run_pol
    from fracture_plotter.regular_fracture.visualization.pot import run_pot

    run_pol(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )
    run_pot(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )

    files = [
        os.path.join(paths.tex_dir, "pot_cond_0"),
    ]
    run_overlay(paths, files)


def run_all_small_features(paths):
    # from fracture_plotter.small_features.visualization.boundarydata import run_boundary_data
    from fracture_plotter.small_features.visualization.pol import run_pol
    from fracture_plotter.small_features.visualization.pot import run_pot

    run_pol(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )

    # TODO: Fix this if needed
    # run_boundary_data(places_and_methods)
    # print("Finished running boundary data")

    run_pot(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )

    files = [
        os.path.join(paths.tex_dir, f"pol_p_line_0"),
        os.path.join(paths.tex_dir, f"pot_fracture_3"),
    ]
    run_overlay(paths, files)


def run_all_field_case(paths):
    from fracture_plotter.field_case.visualization.pol import run_pol
    from fracture_plotter.field_case.visualization.pot import run_pot

    run_pol(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )
    run_pot(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )

    files = [
        os.path.join(paths.tex_dir, "pol_line_0"),
        os.path.join(paths.tex_dir, "pol_line_1"),
        os.path.join(paths.tex_dir, "pot"),
    ]
    run_overlay(paths, files)


def main():
    paths = get_paths(__file__)
    if comp_mean_std:
        compute_mean_and_std(methods_mean_std)

    subdir_list = csv_tools.find_direct_subdirectories(paths.module_dir)
    for subdir in subdir_list:
        case = subdir.split(os.sep)[-1]
        if case in case_list:
            if create_pdfs:
                # Get the path to the pol.py file in the visualization directory for this case as a reference
                file_handle = os.path.join(subdir, "visualization", "pol.py")
                paths = get_paths(file_handle)

                if case == "single_fracture":
                    run_all_single_fracture(paths)
                elif case == "regular_fracture":
                    run_all_regular_fracture(paths)
                elif case == "small_features":
                    run_all_small_features(paths)
                elif case == "field_case":
                    run_all_field_case(paths)


if __name__ == "__main__":
    main()
