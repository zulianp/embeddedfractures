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

# Configuration for each case
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
            {
                "func": "run_pot",
                "module": "pot",
                "filter": "create_places_and_methods_dict",
            },
        ],
        "overlay_files": ["pot_cond_0"],
    },
    "small_features": {
        "functions": [
            {
                "func": "run_pol",
                "module": "pol",
                "filter": "create_places_and_methods_dict",
            },
            {
                "func": "run_pot",
                "module": "pot",
                "filter": "create_places_and_methods_dict",
            },
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


def run_case(paths, case, places_and_methods, refinement_indices=None, titles=None):
    config = case_config[case]
    funcs = {}
    modules = {}

    # Pre-import and cache modules for efficiency
    for entry in config["functions"]:
        mod = modules.setdefault(
            entry["module"],
            importlib.import_module(
                f"fracture_plotter.{case}.visualization.{entry['module']}"
            ),
        )
        funcs[entry["func"]] = getattr(mod, entry["func"])

    for entry in config["functions"]:
        if entry["func"] in {"run_pol", "run_pot"}:
            places_and_methods_dict = None
            if "filter" in entry:
                mod = modules[entry["module"]]
                filter_func = getattr(mod, entry["filter"])
                places_and_methods_dict = filter_func(
                    refinement_indices, places_and_methods, paths
                )
            if refinement_indices is not None:
                funcs[entry["func"]](
                    (
                        places_and_methods
                        if places_and_methods_dict is None
                        else places_and_methods_dict
                    ),
                    fontsize,
                    subfig_fontsize,
                    refinement_indices=refinement_indices,
                    titles=titles,
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
    refinement_indices_by_case=None,
    titles_by_case=None,
):
    if methods_mean_std is None:
        methods_mean_std = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]

    paths = get_paths(__file__)

    if COMP_MEAN_STD:
        compute_mean_and_std(methods_mean_std)

    focus_inst, focus_meth = get_focus_institute_and_method(current=current)
    places_and_methods = {focus_inst: [focus_meth], "mean": ["key"]}

    subdirs = csv_tools.find_direct_subdirectories(paths.module_dir)
    for subdir in subdirs:
        case = os.path.basename(subdir)
        if case in case_list and CREATE_PDFS:
            file_handle = os.path.join(subdir, "visualization", "pol.py")
            case_paths = get_paths(file_handle)
            run_case(
                case_paths,
                case,
                places_and_methods,
                refinement_indices_by_case.get(case),
                titles_by_case.get(case),
            )

    if COPY_PDFS_TO_OVERLEAF:
        src_dir = Path(paths.module_dir).parent.parent / "plots"
        github_dir = Path(paths.module_dir).parent.parent.parent
        dst_dir = os.path.join(Path(github_dir), "overleaf_embedded_fractures/plots")
        for case in os.listdir(src_dir):
            if case in case_list:
                src = os.path.join(src_dir, case)
                dst = os.path.join(dst_dir, case)
                shutil.copytree(src, dst, dirs_exist_ok=True)


if __name__ == "__main__":
    run_all()
