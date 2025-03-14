import os
import re
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def get_num_rows(csv_file: str):
    with open(csv_file, 'r') as f:
        return sum(1 for line in f)

def get_max_num_rows(csv_files: list):
    max_num_rows = -1
    for csv_file in csv_files:
        num_rows = get_num_rows(csv_file)
        if num_rows > max_num_rows:
            max_num_rows = num_rows
    return max_num_rows

def find_common_min_max_integer_in_filenames(base_dir: str, methods_included: list, pattern: str = 'dol_refinement_*.csv'):
    common_max_int = None
    common_min_int = None
    regex_pattern = re.escape(pattern).replace('\\*', r'(\d+)')

    for method in methods_included:
        method_dir = os.path.join(base_dir, method)
        method_max_int = None
        method_min_int = None

        for root, dirs, files in os.walk(method_dir):
            for file in files:
                match = re.match(regex_pattern, file)
                if match:
                    num = int(match.group(1))
                    if method_max_int is None or num > method_max_int:
                        method_max_int = num
                    if method_min_int is None or num < method_min_int:
                        method_min_int = num

        # Update common_min_int and common_max_int based on the current method's min/max
        if common_max_int is None or method_max_int < common_max_int:
            common_max_int = method_max_int
        if common_min_int is None or method_min_int > common_min_int:
            common_min_int = method_min_int

    return common_min_int, common_max_int

def extract_institute_and_method(filename):
    parts = filename.split('/')
    institute_method = '/'.join(parts[-3:-1]) # Extract the second last and third last parts
    return institute_method

def filter_csv_files(csv_files, methods_included):
    filtered_csv_files = []
    institutes_and_methods = [extract_institute_and_method(filename) for filename in csv_files]
    for i, csv_file in enumerate(csv_files):
        if institutes_and_methods[i] in methods_included:
            filtered_csv_files.append(csv_file)
    return filtered_csv_files

def find_csv_filenames(base_dir: str, focus_dir: str = "USI/FEM_LM", filename: str = 'results.csv'):
    csv_files = []
    focus_file = None
    focus_dir = os.path.join(base_dir, focus_dir)
    
    for root, dirs, files in os.walk(base_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            if os.path.abspath(root) == os.path.abspath(focus_dir):
                focus_file = file_path  # Save the focus_dir file to add it first
            else:
                # Exclude any previously computed mean and standard deviation files
                if not('mean' in root or 'std' in root):
                    csv_files.append(file_path)
    
    # Place the focus_dir file at the beginning of the list, if it was found
    if focus_file:
        csv_files.insert(0, focus_file)
    
    return csv_files

def find_direct_subdirectories(base_dir: str):
    subdirectories = [f.path for f in os.scandir(base_dir) if f.is_dir()]
    subdirectories.sort()  # Sort the subdirectories alphabetically
    return subdirectories

def create_interpolated_dfs(df_list):
    ref_df = df_list[0]
    interpolated_dfs = [ref_df]

    for other_df in df_list[1:]:
        # Extract x-values from the reference CSV
        ref_x = ref_df.iloc[:, 0].values  # Assuming x-values are in the first column

        # Extract x-values and y-values from the other CSV
        other_x = other_df.iloc[:, 0].values
        other_y = other_df.iloc[:, 1:].values  # All columns except the first

        # Ensure other_x is sorted for interpolation
        sort_idx = np.argsort(other_x)
        other_x_sorted = other_x[sort_idx]
        other_y_sorted = other_y[sort_idx, :]

        # Prepare for interpolation by handling duplicate x-values
        interpolated_y = np.empty((len(ref_x), other_y.shape[1]))

        for i in range(other_y.shape[1]):
            # Create DataFrame for x and y
            data_df = pd.DataFrame({'x': other_x_sorted, 'y': other_y_sorted[:, i]})

            # Group by x and compute mean y-values to handle duplicates
            data_df = data_df.groupby('x', as_index=False).mean()

            # Extract unique x-values and corresponding y-values
            other_x_unique = data_df['x'].values
            other_y_unique = data_df['y'].values

            # Create an interpolation function using cubic interpolation
            f = interp1d(other_x_unique, other_y_unique, kind='linear', fill_value='extrapolate')

            # Interpolate to ref_x
            interpolated_y[:, i] = f(ref_x)

        # Combine ref_x with interpolated data
        interpolated_df = pd.DataFrame(np.column_stack((ref_x, interpolated_y)))
        interpolated_dfs.append(interpolated_df)

    return interpolated_dfs

def create_mean_and_std_csv_files(base_dir: str, pattern_filename: str, focus_dir: str = "USI/FEM_LM", methods_included: list[str] = ["USI/FEM_LM"]):
    min_int_in_filenames, max_int_in_filenames = (0, 0)
    if '*' in pattern_filename:
        min_int_in_filenames, max_int_in_filenames = find_common_min_max_integer_in_filenames(base_dir=base_dir, methods_included=methods_included, pattern=pattern_filename)

    for ref in range(min_int_in_filenames, max_int_in_filenames + 1):
        filename = pattern_filename.replace('*', str(ref)) if '*' in pattern_filename else pattern_filename
        # Collect all the CSV files with the same name in any (recursive) subdirectory of base_dir
        # csv_files[0] corresponds to that in the focus_dir
        csv_files = filter_csv_files(find_csv_filenames(base_dir=base_dir, filename=filename, focus_dir=focus_dir), list(set(["USI/FEM_LM"] + methods_included)))

        # Create combined DataFrame
        dfs = create_interpolated_dfs(df_list=[pd.read_csv(file, header=None) for file in csv_files])
        # TODO: once ours is OK, include in mean and std computations
        combined_df = pd.concat(dfs[1:], ignore_index=True).sort_values(by=dfs[1].columns[0]).reset_index(drop=True)

        # Compute the mean and standard deviation (assumes the first column is the reference)
        mean_df = combined_df.groupby(combined_df.columns[0]).mean().reset_index()
        std_df = combined_df.groupby(combined_df.columns[0]).std().reset_index()

        # Save mean and standard deviation to CSV files
        for stat, dir_name in [('mean', 'mean/key'), ('std', 'std/key')]:
            stat_dir = os.path.join(base_dir, dir_name)
            os.makedirs(stat_dir, exist_ok=True)
            (mean_df if stat == 'mean' else std_df).to_csv(os.path.join(stat_dir, filename), index=False, header=False)
