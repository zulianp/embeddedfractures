import importlib
import os
import shutil
from pathlib import Path

import fracture_plotter.utils.csv as csv_tools
from fracture_plotter.utils.compute_mean_and_std_all import compute_mean_and_std
from fracture_plotter.utils.general import (
    get_focus_institute_and_method,
    get_paths,
    process_args,
)
from fracture_plotter.utils.overlay import run_overlay
from fracture_plotter.utils.plot_routines import fontsize, subfig_fontsize

# Settings
comp_mean_std = True
methods_mean_std = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]
focus_inst, focus_meth = get_focus_institute_and_method(current=True)
create_pdfs = True
places_and_methods = {focus_inst: [focus_meth], "mean": ["key"]}
case_list = ["single_fracture", "regular_fracture", "small_features", "field_case"]
copy_pdfs_to_overleaf = True

# Configuration for each case: list of functions with their submodules and overlay files.
case_config = {
    "single_fracture": {
        "functions": [
            {"func": "run_percentiles", "module": "percentiles"},
            {"func": "run_pol", "module": "pol"},
            {"func": "run_pot", "module": "pot"},
        ],
        "overlay_files": [
            "pol_c_fracture",
            "pol_c_matrix",
            "pol_p_matrix",
            "pot_outflux",
        ],
    },
    "regular_fracture": {
        "functions": [
            {"func": "run_pol", "module": "pol"},
            {"func": "run_pot", "module": "pot"},
        ],
        "overlay_files": ["pot_cond_0"],
    },
    "small_features": {
        "functions": [
            {"func": "run_pol", "module": "pol"},
            {"func": "run_pot", "module": "pot"},
        ],
        "overlay_files": ["pol_p_line_0", "pot_fracture_3"],
    },
    "field_case": {
        "functions": [
            {"func": "run_pol", "module": "pol"},
            {"func": "run_pot", "module": "pot"},
        ],
        "overlay_files": ["pol_line_0", "pol_line_1", "pot"],
    },
}


def run_all_case(paths, case):
    config = case_config[case]
    funcs = {}
    for entry in config["functions"]:
        # Dynamically import from the correct submodule.
        module = importlib.import_module(
            f"fracture_plotter.{case}.visualization.{entry['module']}"
        )
        funcs[entry["func"]] = getattr(module, entry["func"])

    # Execute functions in order.
    for entry in config["functions"]:
        funcs[entry["func"]](places_and_methods, fontsize, subfig_fontsize)

    files = [os.path.join(paths.tex_dir, name) for name in config["overlay_files"]]
    run_overlay(paths, files)


def main():
    paths = get_paths(__file__)
    if comp_mean_std:
        compute_mean_and_std(methods_mean_std)

    if create_pdfs:
        subdir_list = csv_tools.find_direct_subdirectories(paths.module_dir)
        for subdir in subdir_list:
            case = os.path.basename(subdir)
            if case in case_list and create_pdfs:
                file_handle = os.path.join(subdir, "visualization", "pol.py")
                case_paths = get_paths(file_handle)
                run_all_case(case_paths, case)

    if copy_pdfs_to_overleaf:
        src_dir = Path(paths.module_dir).parent.parent / "plots"
        github_dir = Path(paths.module_dir).parent.parent.parent
        dst_dir = os.path.join(Path(github_dir), "overleaf_embedded_fractures/plots")
        for subdir in os.listdir(src_dir):
            if subdir in case_list:
                src = os.path.join(src_dir, subdir)
                dst = os.path.join(dst_dir, subdir)
                shutil.copytree(src, dst, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
