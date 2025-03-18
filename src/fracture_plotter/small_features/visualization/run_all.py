# Source: https://git.iws.uni-stuttgart.de/benchmarks/fracture-flow-3d
import os

from boundarydata import run_boundary_data
from pol import run_pol
from pot import run_pot

from fracture_plotter.utils.general import get_paths, process_args
from fracture_plotter.utils.overlay import run_overlay
from fracture_plotter.utils.plot_routines import fontsize, subfig_fontsize


def run_all():
    paths = get_paths(__file__)

    places_and_methods = process_args()
    print(f"Running all scripts in sequence for case {paths.case}...")

    run_pol(places_and_methods, fontsize=fontsize, subfig_fontsize=subfig_fontsize)
    print("Finished running pol")

    # TODO: Fix this if needed
    # run_boundary_data(places_and_methods)
    # print("Finished running boundary data")

    run_pot(
        places_and_methods=places_and_methods,
        fontsize=fontsize,
        subfig_fontsize=subfig_fontsize,
    )
    print("Finished running pot")

    files = [
        os.path.join(paths.tex_dir, f"pol_p_line_0"),
        os.path.join(paths.tex_dir, f"pot_fracture_3"),
    ]
    run_overlay(files, paths)
    print("Finished running overlay")


if __name__ == "__main__":
    run_all()
