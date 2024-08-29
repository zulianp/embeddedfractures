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

def find_csv_filenames(base_dir: str, focus_dir: str = "USI", filename: str = 'results.csv'):
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
                csv_files.append(file_path)
    
    # Place the focus_dir file at the beginning of the list, if it was found
    if focus_file:
        csv_files.insert(0, focus_file)
    
    return csv_files

def find_max_integer_in_filenames(base_dir: str, pattern:str ='dol_refinement_*.csv'):
    """
    Find the maximum integer X seen in filenames matching a specific pattern (e.g., dol_refinement_X.csv)
    within a directory and its subdirectories.

    Parameters:
    - base_dir (str): The base directory to start searching for files.
    - pattern (str): The pattern to match filenames. The default is 'dol_refinement_*.csv'.

    Returns:
    - max_int (int or None): The maximum integer X found in matching filenames, or None if no such filenames are found.
    """
    max_int = None
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
    return max_int

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

# Function to interpolate and align the data based on the first column
def interpolate_and_align(df_list: list):
    reference_df = df_list[0]
    ref_column = reference_df.iloc[:, 0].values
    
    interpolated_dfs = []
    for idx, df in enumerate(df_list[1:]):
        x = df.iloc[:, 0].values
        
        # Create an interpolator for each column (except the first)
        interpolated_values = []
        for i in range(1, df.shape[1]):
            interpolator = interp1d(x, df.iloc[:, i].values, kind='linear', fill_value="extrapolate")
            interpolated_values.append(interpolator(ref_column))
        
        # Combine the interpolated values with the reference x values
        interpolated_df = pd.DataFrame(np.column_stack([ref_column] + interpolated_values))
        interpolated_df.columns = reference_df.columns

        interpolated_dfs.append(interpolated_df)
    
    return [reference_df] + interpolated_dfs

def create_df_from_csv(file: str, num_cols: int = None, column_names = None):
    def convert_to_float(s):
        try:
            return float(s.decode().replace('D', 'e'))
        except ValueError:
            return s.decode()

    # Load the first row to check for a header
    first_row_df = pd.read_csv(file, header=None, nrows=1)
    first_row = first_row_df.iloc[0].apply(lambda x: isinstance(x, str))
    # Number of valid columns to read
    num_valid_columns = first_row_df.notna().sum(axis=1).iloc[0] if num_cols is None else num_cols

    if first_row.any():
        # If any entry in the first row is a string, it's likely a header
        df = pd.read_csv(file, usecols=range(num_valid_columns), converters={i: lambda x: convert_to_float(x.encode()) for i in range(num_valid_columns)})
    else:
        # No header present, treat all data as numeric
        df = pd.read_csv(file, header=None, usecols=range(num_valid_columns), converters={i: lambda x: convert_to_float(x.encode()) for i in range(num_valid_columns)})
    
    # Convert all columns to numeric, ignoring any headers
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    # Set a header if it doesn't exist and set it to the provided column names
    if column_names is not None:
        df.columns = column_names
    
    return df

def create_interpolated_dfs_from_csv_files(csv_files: list):
    focus_df = create_df_from_csv(csv_files[0])
    df_list = [create_df_from_csv(file=file, num_cols=focus_df.shape[1], column_names=focus_df.columns) for file in csv_files[1:]]
    df_list.insert(0, focus_df)

    return interpolate_and_align(df_list)

def create_mean_and_std_csv_files(base_dir: str, pattern_filename: str, focus_dir: str = "USI"):
    max_ref_num = find_max_integer_in_filenames(os.path.join(base_dir, focus_dir))  
    if max_ref_num is None:
        max_ref_num = 0

    for ref in range(0, max_ref_num + 1):
        filename = pattern_filename.replace('*', str(ref))

        # Collect all the CSV files with the same name in base_dir, their subdirectories, their subdirectories, etc.
        # csv_files[0] will correspond to that in the focus_dir
        csv_files = find_csv_filenames(base_dir=base_dir, filename=filename)
        
        # Create Pandas DataFrames from the CSV files
        dfs = create_interpolated_dfs_from_csv_files(csv_files=csv_files)

        # Combine the dataframes
        combined_df = pd.concat(dfs, ignore_index=True)

        # Ensure the first column is numeric and the other columns are consistent
        combined_df.iloc[:, 0] = pd.to_numeric(combined_df.iloc[:, 0], errors='coerce')
        for col in combined_df.columns[1:]:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

        # Sort by the first column to ensure proper alignment during groupby
        combined_df = combined_df.sort_values(by=combined_df.columns[0]).reset_index(drop=True)

        # Compute the mean (assumes the first column is the reference)
        mean_df = combined_df.groupby(combined_df.columns[0]).mean().reset_index()

        # Compute the standard deviation using the custom formula
        std_df = combined_df.groupby(combined_df.columns[0]).std().reset_index()

        # Create a mean_and_std directory if it doesn't exist
        mean_and_std_dir = os.path.join(base_dir, 'mean_and_std')
        if not os.path.exists(mean_and_std_dir):
            os.makedirs(mean_and_std_dir)

        # Save the mean and standard deviation DataFrames to CSV files
        mean_df.to_csv(os.path.join(mean_and_std_dir, filename.replace('.csv', '') + '_mean.csv'), index=False, header=False)
        std_df.to_csv(os.path.join(mean_and_std_dir, filename.replace('.csv', '') + '_std.csv'), index=False, header=False)

        
