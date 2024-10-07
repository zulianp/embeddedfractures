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

    # Ensure ref_column is sorted and unique
    ref_column = np.unique(ref_column)

    interpolated_dfs = []
    for idx, df in enumerate(df_list[1:]):
        x = df.iloc[:, 0].values

        # Create an interpolator for each column (except the first)
        interpolated_values = []
        for i in range(1, df.shape[1]):
            interpolator = interp1d(
                x,
                df.iloc[:, i].values,
                kind='linear',
                bounds_error=False,
                fill_value=np.nan
            )
            interpolated_values.append(interpolator(ref_column))

        # Combine the interpolated values with the reference x values
        interpolated_df = pd.DataFrame(
            np.column_stack([ref_column] + interpolated_values)
        )
        interpolated_dfs.append(interpolated_df)

    return [reference_df] + interpolated_dfs


def create_df_from_csv(file: str, num_cols: int = None, column_names=None):
    def convert_to_float(s):
        try:
            return float(s.replace('D', 'e'))
        except ValueError:
            return s

    # Read the first few rows to sample data
    sample_df = pd.read_csv(file, header=None, nrows=5)

    # Check if the first row contains non-numeric strings
    first_row = sample_df.iloc[0]

    # Attempt to convert the first row to numeric values
    numeric_first_row = pd.to_numeric(first_row, errors='coerce')
    # Identify non-numeric entries
    non_numeric_in_first_row = numeric_first_row.isna()

    # Check if subsequent rows are mostly numeric
    subsequent_rows = sample_df.iloc[1:]
    # Convert the DataFrame to numeric, non-convertible values become NaN
    numeric_subsequent_rows = subsequent_rows.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
    # Check if all values in each row are numeric (not NaN)
    numeric_in_subsequent_rows = numeric_subsequent_rows.notna().all(axis=1)

    # Decide if header exists
    has_header = False
    if non_numeric_in_first_row.any() and numeric_in_subsequent_rows.sum() >= len(subsequent_rows) - 1:
        has_header = True

    # Now read the full CSV with the detected header
    header = 0 if has_header else None
    df = pd.read_csv(
        file,
        header=header,
        converters={i: convert_to_float for i in range(num_cols)} if num_cols else None,
        usecols=range(num_cols) if num_cols else None
    )

    # Convert columns to numeric where appropriate
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    # Sort the DataFrame by the first column if it's numeric
    if pd.api.types.is_numeric_dtype(df[df.columns[0]]):
        df = df.sort_values(by=df.columns[0]).reset_index(drop=True)

    # Set column names if provided
    if column_names is not None:
        df.columns = column_names

    return df


def is_float(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def standardize_dataframe(df):
    # Ensure consistent data types
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])

    # Convert column names to strings for consistency
    df.columns = df.columns.astype(str)

    return df

def create_interpolated_dfs_from_csv_files(csv_files: list):
    df_list = [create_df_from_csv(file) for file in csv_files]

    # Standardize all DataFrames
    df_list = [standardize_dataframe(df) for df in df_list]

    # Get the intersection of all column names
    common_columns = set(df_list[0].columns)
    for df in df_list[1:]:
        common_columns = common_columns.intersection(df.columns)
    common_columns = sorted(common_columns)

    # Select only the common columns
    df_list = [df[common_columns] for df in df_list]

    # Ensure all DataFrames have the same number of rows
    min_num_rows = min([df.shape[0] for df in df_list])
    df_list = [df.iloc[:min_num_rows].reset_index(drop=True) for df in df_list]

    return interpolate_and_align(df_list)

def exclude_some_csv_files(filenames):
    filtered_filenames = []
    for filename in filenames:
        if not ("LANL" in filename and "MFD/" in filename) and not ("USTUTT" in filename and ("TPFA/" in filename or "BOX" in filename)):
            filtered_filenames.append(filename)
    return filtered_filenames

def create_mean_and_std_csv_files(base_dir: str, pattern_filename: str, focus_dir: str = "USI/FEM_LM"):
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
        csv_files = find_csv_filenames(base_dir=base_dir, filename=filename)
        csv_files = exclude_some_csv_files(csv_files)
        
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

        
