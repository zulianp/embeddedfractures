import os

from percentiles import run_percentiles
from pol import run_pol
from pot import run_pot

from fracture_plotter.utils.general import get_paths, process_args
from fracture_plotter.utils.overlay import run_overlay


def run_all():
    paths = get_paths(__file__)
    fontsize = 30
    subfig_fontsize = 24

    places_and_methods = process_args()
    print(f"Running all scripts in sequence for case {paths.case}...")

    run_percentiles(
        places_and_methods, fontsize=fontsize, subfig_fontsize=subfig_fontsize
    )
    print("Finished running percentiles")

    run_pol(places_and_methods, fontsize=fontsize, subfig_fontsize=subfig_fontsize)
    print("Finished running pol")

    run_pot(places_and_methods, fontsize=fontsize, subfig_fontsize=subfig_fontsize)
    print("Finished running pot")

    files = [
        os.path.join(paths.tex_dir, f"{paths.case}_pol_c_fracture"),
        os.path.join(paths.tex_dir, f"{paths.case}_pol_c_matrix"),
        os.path.join(paths.tex_dir, f"{paths.case}_pol_p_matrix"),
        os.path.join(paths.tex_dir, f"{paths.case}_pot_outflux"),
    ]

    run_overlay(files, paths)
    print("Finished running overlay")


if __name__ == "__main__":
    run_all()
