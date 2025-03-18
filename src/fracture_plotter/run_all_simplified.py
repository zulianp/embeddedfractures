import json
import os

import fracture_plotter.utils.csv as csv_tools
from fracture_plotter.utils.compute_mean_and_std_all import compute_mean_and_std
from fracture_plotter.utils.general import get_focus_institute_and_method, get_paths

comp_mean_std = True  # compute the mean and std of the results
methods_mean_std = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]
focus_inst, focus_meth = get_focus_institute_and_method(current=True)

create_pdfs = True  # create plots in PDF format
places_and_methods = {focus_inst: [focus_meth], "mean": ["key"]}
places_and_methods_str = json.dumps(places_and_methods)


def main():
    paths = get_paths(__file__)
    if comp_mean_std:
        compute_mean_and_std(methods_mean_std)

    subdir_list = csv_tools.find_direct_subdirectories(paths.module_dir)
    for subdir in subdir_list:
        case = subdir.split(os.sep)[-1][0]
        case = int(case) if case.isdigit() else -1
        if case in [1, 2, 3, 4]:
            if create_pdfs:
                print(f"Changing directory to {subdir} and running run_all.py there")
                file_handle = os.path.join(subdir, "visualization", "run_all.py")


if __name__ == "__main__":
    main()
