from enum import Enum

from fracture_plotter.run_all import run_all


class Case(Enum):
    SINGLE_FRACTURE = "single_fracture"
    REGULAR_FRACTURE = "regular_fracture"
    SMALL_FEATURES = "small_features"
    FIELD_CASE = "field_case"


def main():
    # Use the enum values to build the case_list
    # case_list = [case.value for case in Case]
    case_list = Case.REGULAR_FRACTURE.value

    refinement_indices_by_case = {
        Case.SINGLE_FRACTURE.value: [0, 1, 2],
        Case.REGULAR_FRACTURE.value: [0, 1, 2],
        Case.SMALL_FEATURES.value: [0, 1, 2],
        Case.FIELD_CASE.value: None,
    }

    titles_by_case = {
        Case.SINGLE_FRACTURE.value: ["Title 0", "Title 1", "Title 2"],
        Case.REGULAR_FRACTURE.value: ["Title 0", "Title 1", "Title 2"],
        Case.SMALL_FEATURES.value: ["Title 0", "Title 1", "Title 2"],
        Case.FIELD_CASE.value: None,
    }

    # Check that the length of each title by case is the same length as the refinment indices by case
    for case in Case:
        if titles_by_case[case.value] is not None:
            assert len(titles_by_case[case.value]) == len(
                refinement_indices_by_case[case.value]
            ), f"Title list length does not match refinement indices length for {case.value}"

    # Methods to consider for the mean and standard deviation computation
    methods_mean_std = ["UiB/TPFA", "UiB/MPFA", "UiB/MVEM", "UiB/RT0"]

    run_all(
        current=True,  # True (USI 2024/2025 results), False (ETHZ-USI results)
        methods_mean_std=methods_mean_std,
        case_list=case_list,
        refinement_indices_by_case=refinement_indices_by_case,
        titles_by_case=titles_by_case,
    )


if __name__ == "__main__":
    main()
