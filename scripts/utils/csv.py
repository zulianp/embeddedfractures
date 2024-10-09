import os
import re
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from functools import reduce

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

def find_min_max_integer_in_filenames(base_dir: str, pattern: str = 'dol_refinement_*.csv'):
    max_int = None
    min_int = None
    regex_pattern = re.escape(pattern).replace('\\*', r'(\d+)')

    num_matches = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            match = re.match(regex_pattern, file)
            if match:
                num_matches += 1
                num = int(match.group(1))
                if max_int is None or num > max_int:
                    max_int = num
                if min_int is None or num < min_int:
                    min_int = num

    return min_int, max_int

def extract_institute_and_method(filename):
    # Split the string by '/'
    parts = filename.split('/')

    # Extract the second last and third last parts
    institute_method = '/'.join(parts[-3:-1])
    return institute_method

def filter_csv_files(csv_files, methods_included):
    filtered_csv_files = []
    institutes_and_methods = [extract_institute_and_method(filename) for filename in csv_files]
    for i, csv_file in enumerate(csv_files):
        if institutes_and_methods[i] in methods_included:
            filtered_csv_files.append(csv_file)
    return filtered_csv_files

def find_csv_filenames(base_dir: str, focus_dir: str = "USI/FEM_LM", filename: str = 'results.csv'):
    """
    Find all CSV files with a given filename in a directory and its subdirectories.

    Parameters:
    - base_dir (str): The base directory to start searching for CSV files.
    - focus_dir (str): The directory whose corresponding CSV file should be listed first.
    - filename (str): The name of the CSV file to search for. Default is 'results.csv'.

    Returns:
    - csv_files (list): A list of file paths to the found CSV files, with the file from focus_dir listed first.
    """
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
    """
    Find all direct subdirectories of a given directory.

    Parameters:
    - base_dir (str): The base directory to search for subdirectories.

    Returns:
    - subdirectories (list): A list of the direct subdirectories of the base directory, sorted alphabetically.
    """
    subdirectories = [f.path for f in os.scandir(base_dir) if f.is_dir()]
    subdirectories.sort()  # Sort the subdirectories alphabetically
    return subdirectories

def create_interpolated_dfs(df_list):
    ref_df = df_list[0]

    interpolated_dfs = [ref_df]
    for other_df in df_list[1:]:
        # Step 2: Extract x-values from the reference CSV
        ref_x = ref_df.iloc[:, 0].values  # Assuming x-values are in the first column

        # Extract x-values and y-values from the other CSV
        other_x = other_df.iloc[:, 0].values
        other_y = other_df.iloc[:, 1:].values  # All columns except the first

        # Ensure other_x is sorted for interpolation
        sort_idx = np.argsort(other_x)
        other_x_sorted = other_x[sort_idx]
        other_y_sorted = other_y[sort_idx, :]

        # Step 3: Interpolate the other CSV's data to the reference x-values
        interpolated_y = np.empty((len(ref_x), other_y.shape[1]))

        for i in range(other_y.shape[1]):
            # Create an interpolation function for each column
            f = interp1d(other_x_sorted, other_y_sorted[:, i], kind='cubic', fill_value='extrapolate')
            # Interpolate to ref_x
            interpolated_y[:, i] = f(ref_x)

        # Step 4: Combine ref_x with interpolated data
        interpolated_df = pd.DataFrame(np.column_stack((ref_x, interpolated_y)))

        # Optionally, set column names if known
        interpolated_df.columns = ref_df.columns

        interpolated_dfs.append(interpolated_df)
    return interpolated_dfs

def create_mean_and_std_csv_files(base_dir: str, pattern_filename: str, focus_dir: str = "USI/FEM_LM", methods_included: list[str] = ["USI/FEM_LM"]):
    min_int_in_filenames = None 
    max_int_in_filenames = None 
    if '*' in pattern_filename:
        min_int_in_filenames, max_int_in_filenames = find_min_max_integer_in_filenames(base_dir=os.path.join(base_dir, focus_dir), pattern=pattern_filename)  
    
    if min_int_in_filenames is None:
        min_int_in_filenames = 0

    if max_int_in_filenames is None:
        max_int_in_filenames = 0

    for ref in range(min_int_in_filenames, max_int_in_filenames + 1):
        if '*' in pattern_filename:
            filename = pattern_filename.replace('*', str(ref))
        else:
            filename = pattern_filename

        # Collect all the CSV files with the same name in base_dir, their subdirectories, their subdirectories, etc.
        # csv_files[0] will correspond to that in the focus_dir
        csv_files = filter_csv_files(find_csv_filenames(base_dir=base_dir, filename=filename), methods_included)

        # Create Pandas DataFrames from the CSV files
        dfs = create_interpolated_dfs(df_list=[pd.read_csv(file, header=None) for file in csv_files])

        # Combine the dataframes
        combined_df = pd.concat(dfs[1:], ignore_index=True) # TODO: once ours is OK, include in mean and std computations

        # Ensure the first column is numeric and the other columns are consistent
        combined_df.iloc[:, 0] = pd.to_numeric(combined_df.iloc[:, 0], errors='coerce')
        for col in combined_df.columns[1:]:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

        # Sort by the first column to ensure proper alignment during groupby
        combined_df = combined_df.sort_values(by=combined_df.columns[0]).reset_index(drop=True)

        # Compute the mean (assumes the first column is the reference)
        mean_df = combined_df.groupby(combined_df.columns[0]).mean().reset_index()

        # Compute the standard deviation (assumes the first column is the reference)
        std_df = combined_df.groupby(combined_df.columns[0]).std().reset_index()
        
        # Create a mean_and_std directory if it doesn't exist
        mean_dir = os.path.join(base_dir, 'mean/key')
        if not os.path.exists(mean_dir):
            os.makedirs(mean_dir)

        std_dir = os.path.join(base_dir, 'std/key')
        if not os.path.exists(std_dir):
            os.makedirs(std_dir)

        # Save the mean and standard deviation DataFrames to CSV files
        mean_csv_filename = os.path.join(mean_dir, filename)
        std_csv_filename = os.path.join(std_dir, filename)
        mean_df.to_csv(mean_csv_filename, index=False, header=False)
        std_df.to_csv(std_csv_filename, index=False, header=False)

        
