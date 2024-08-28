import pandas as pd
import os
import numpy as np
from scipy.interpolate import interp1d

def find_csv_files(base_dir, filename='results.csv'):
    csv_files = []
    for root, dirs, files in os.walk(base_dir):
        if filename in files:
            csv_files.append(os.path.join(root, filename))
    return csv_files

# Function to detect if a file has a header and load the CSV file accordingly
def load_and_align_csv(file):
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

# Define the top-level directories
top_level_directories = ['dummy_tests/A', 'dummy_tests/B', 'dummy_tests/C']

# Collect all the results.csv files
csv_files = []
for directory in top_level_directories:
    csv_files.extend(find_csv_files(directory))

# Load and align all the CSV files
dfs = [load_and_align_csv(file) for file in csv_files]

# Filter out any None values in case there was an error loading a file
dfs = [df for df in dfs if df is not None]

# Perform interpolation and alignment on the loaded DataFrames
aligned_dfs = interpolate_and_align(dfs)

# Combine the dataframes
combined_df = pd.concat(aligned_dfs, ignore_index=True)

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
reference_column = 'reference'
mean_df.columns = [f'{col}_mean' if col != 0 else reference_column for col in mean_df.columns]
std_df.columns = [f'{col}_std' if col != 0 else reference_column for col in std_df.columns]

# Merge the mean and standard deviation into a single DataFrame
result_df = pd.merge(mean_df, std_df, on=reference_column)

# Save the combined dataframe to a new CSV file
result_df.to_csv('dummy_tests/combined_mean_std_results.csv', index=False, header=False)

# Display the result
print(result_df)
