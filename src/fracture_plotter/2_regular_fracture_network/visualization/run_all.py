import os

from pol import run_pol
from pot import run_pot

from fracture_plotter.utils.general import get_paths, process_args
from fracture_plotter.utils.overlay import run_overlay


def run_all():
    fontsize = 30
    subfig_fontsize = 25

    paths = get_paths(__file__)

    places_and_methods = process_args()
    print(f"Running all scripts in sequence for case {paths.case}...")

    run_pol(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )
    print("Finished running pol")

    run_pot(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )
    print("Finished running pot")

    files = [
        os.path.join(paths.tex_dir, f"{paths.case}_pot_cond_0"),
        # os.path.join(paths.tex_dir, "overlay_fig1"),
    ]
    run_overlay(files, paths)
    print("Finished running overlay")


if __name__ == "__main__":
    run_all()
