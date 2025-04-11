import importlib
import os
import shutil
from pathlib import Path

import fracture_plotter.utils.csv as csv_tools
from fracture_plotter.utils.compute_mean_and_std_all import compute_mean_and_std
from fracture_plotter.utils.general import get_focus_institute_and_method, get_paths
from fracture_plotter.utils.overlay import run_overlay
from fracture_plotter.utils.plot_routines import fontsize, plt, subfig_fontsize

# Fixed settings
COMP_MEAN_STD = True
CREATE_PDFS = True
COPY_PDFS_TO_OVERLEAF = False

# Configuration for each case: list of functions with their submodules and overlay files
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

# Use None for cases where no refinement_index should be passed
refinement_index_by_case = {
    "single_fracture": [0, 1, 2],
    "regular_fracture": [0, 1, 2],
    "small_features": [0, 1],
    "field_case": None,
}


def run_case(paths, case, places_and_methods, refinement_index=None):
    config = case_config[case]
    funcs = {}
    for entry in config["functions"]:
        module = importlib.import_module(
            f"fracture_plotter.{case}.visualization.{entry['module']}"
        )
        funcs[entry["func"]] = getattr(module, entry["func"])
    for entry in config["functions"]:
        if entry["func"] == "run_pol":
            if refinement_index is not None:
                funcs[entry["func"]](
                    places_and_methods,
                    fontsize,
                    subfig_fontsize,
                    refinement_index=refinement_index,
                )
            else:
                funcs[entry["func"]](places_and_methods, fontsize, subfig_fontsize)
        else:
            funcs[entry["func"]](places_and_methods, fontsize, subfig_fontsize)
        plt.close("all")
    files = [os.path.join(paths.tex_dir, name) for name in config["overlay_files"]]
    run_overlay(paths, files)


def run_all(
    current=True,
    methods_mean_std=None,
    case_list=["single_fracture", "regular_fracture", "small_features", "field_case"],
):
    if methods_mean_std is None:
        methods_mean_std = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]

    paths = get_paths(__file__)

    if COMP_MEAN_STD:
        compute_mean_and_std(methods_mean_std)

    focus_inst, focus_meth = get_focus_institute_and_method(current=current)
    places_and_methods = {focus_inst: [focus_meth], "mean": ["key"]}

    subdir_list = csv_tools.find_direct_subdirectories(paths.module_dir)
    for subdir in subdir_list:
        case = os.path.basename(subdir)
        if case in case_list and CREATE_PDFS:
            file_handle = os.path.join(subdir, "visualization", "pol.py")
            case_paths = get_paths(file_handle)
            # Retrieve the refinement index for the case; may be None.
            ref_index = refinement_index_by_case.get(case)
            run_case(case_paths, case, places_and_methods, refinement_index=ref_index)

    if COPY_PDFS_TO_OVERLEAF:
        src_dir = Path(paths.module_dir).parent.parent / "plots"
        github_dir = Path(paths.module_dir).parent.parent.parent
        dst_dir = os.path.join(Path(github_dir), "overleaf_embedded_fractures/plots")
        for subdir in os.listdir(src_dir):
            if subdir in case_list:
                src = os.path.join(src_dir, subdir)
                dst = os.path.join(dst_dir, subdir)
                shutil.copytree(src, dst, dirs_exist_ok=True)


if __name__ == "__main__":
    run_all()
