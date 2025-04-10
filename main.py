# main.py in embeddedfractures
from fracture_plotter.run_all import run_all


def main():
    # Cases to consider
    case_list = ["small_features"]
    # Methods to consider for the mean and standard deviation computation
    methods_mean_std = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]

    run_all(
        current=True,  # True (USI 2024/2025 results), False (ETHZ-USI results)
        methods_mean_std=methods_mean_std,
        case_list=case_list,
    )


if __name__ == "__main__":
    main()
