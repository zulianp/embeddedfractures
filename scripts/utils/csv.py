import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def find_csv_files(base_dir, filename='results.csv'):
    """
    Find all CSV files with a given filename in a directory and its subdirectories.

    Parameters:
    - base_dir (str): The base directory to start searching for CSV files.
    - filename (str): The name of the CSV file to search for. Default is 'results.csv'.

    Returns:
    - csv_files (list): A list of file paths to the found CSV files.
    """
    csv_files = []
    for root, dirs, files in os.walk(base_dir):
        if filename in files:
            csv_files.append(os.path.join(root, filename))
    return csv_files

def find_direct_subfolders(base_dir):
    """
    Find all direct subfolders of a given directory.

    Parameters:
    - base_dir (str): The base directory to search for subfolders.

    Returns:
    - subfolders (list): A list of the direct subfolders of the base directory.
    """
    subfolders = [f.path for f in os.scandir(base_dir) if f.is_dir()]
    return subfolders

def get_base_dir(project_root, file_dirname):
    return os.path.join(project_root, 'results', os.path.basename(file_dirname))

def create_df_from_csv(file):
    def convert_to_float(s):
        try:
            return float(s.decode().replace('D', 'e'))
        except ValueError:
            return s.decode()

    # Load the first row to check for a header
    df = pd.read_csv(file, header=None, nrows=1)
    first_row = df.iloc[0].apply(lambda x: isinstance(x, str))
    
    if first_row.any():
        # If any entry in the first row is a string, it's likely a header
        df = pd.read_csv(file, converters={i: lambda x: convert_to_float(x.encode()) for i in range(len(first_row))})
    else:
        # No header present, treat all data as numeric
        df = pd.read_csv(file, header=None, converters={i: lambda x: convert_to_float(x.encode()) for i in range(len(first_row))})
    
    # Convert all columns to numeric, ignoring any headers
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    
    return df

# Function to interpolate and align the data based on the first column
def interpolate_and_align(df_list):
    # Use the dataframe with the least amount of columns as reference
    reference_df = min(df_list, key=lambda x: x.shape[1])
    ref_column = reference_df.iloc[:, 0].values
    
    interpolated_dfs = []
    
    for df in df_list[1:]:
        x = df.iloc[:, 0].values
        
        # Create an interpolator for each column (except the first)
        interpolated_values = []
        for i in range(1, df.shape[1]):
            interpolator = interp1d(x, df.iloc[:, i].values, kind='linear', fill_value="extrapolate")
            interpolated_values.append(interpolator(ref_column))
        
        # Combine the interpolated values with the reference x values
        interpolated_df = pd.DataFrame(np.column_stack([ref_column] + interpolated_values))
        interpolated_dfs.append(interpolated_df)
    
    return [reference_df] + interpolated_dfs

def create_interpolated_dfs_from_csv_files(csv_files):
    df_list = [create_df_from_csv(file) for file in csv_files]
    min_columns = min(df.shape[1] for df in df_list)
    
    trimmed_df_list = [df.iloc[:, :min_columns] for df in df_list]
    return interpolate_and_align(trimmed_df_list)

def create_mean_and_std_csv_files(base_dir: str, filename: str, reference_column: str):
    # Collect all the CSV files with the same name in base_dir, their subdirectories, their subdirectories, etc.
    csv_files = find_csv_files(base_dir=base_dir, filename=filename)

    # Create Pandas DataFrames from the CSV files
    dfs = create_interpolated_dfs_from_csv_files(csv_files=csv_files)

    # Combine the dataframes
    combined_df = pd.concat(dfs, ignore_index=True)

    # Ensure the first column is numeric and the other columns are consistent
    combined_df[0] = pd.to_numeric(combined_df[0], errors='coerce')
    for col in combined_df.columns[1:]:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

    # Sort by the first column to ensure proper alignment during groupby
    combined_df = combined_df.sort_values(by=[0]).reset_index(drop=True)

    # Compute the mean (assumes the first column is the reference)
    mean_df = combined_df.groupby(0).mean().reset_index()

    # Compute the standard deviation
    std_df = combined_df.groupby(0).agg(lambda x: np.sqrt(np.mean((x - np.mean(x))**2))).reset_index()

    # Rename the columns for clarity (using "reference_column" as the placeholder for the first column)
    mean_df.columns = [f'{col}_mean' if col != 0 else reference_column for col in mean_df.columns]
    std_df.columns = [f'{col}_std' if col != 0 else reference_column for col in std_df.columns]

    # Save the mean and standard deviation DataFrames to CSV files
    mean_df.to_csv(os.path.join(base_dir, filename.replace('.csv', '') + '_mean.csv'), index=False, header=False)
    std_df.to_csv(os.path.join(base_dir, filename.replace('.csv', '') + '_std.csv'), index=False, header=False)

    print(f"Mean df: {mean_df}")
    print(f"Std df: {std_df}")

def get_num_rows(csv_file):
    with open(csv_file, 'r') as f:
        return sum(1 for line in f)

def get_max_num_rows(csv_files):
    max_num_rows = -1
    for csv_file in csv_files:
        num_rows = get_num_rows(csv_file)
        if num_rows > max_num_rows:
            max_num_rows = num_rows
    return max_num_rows