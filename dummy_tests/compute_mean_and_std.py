import pandas as pd
import os
import numpy as np

def find_csv_files(base_dir, filename='results.csv'):
    csv_files = []
    for root, dirs, files in os.walk(base_dir):
        if filename in files:
            csv_files.append(os.path.join(root, filename))
    return csv_files

# Define the top-level directories
top_level_directories = ['dummy_tests/A', 'dummy_tests/B', 'dummy_tests/C']

# Collect all the results.csv files
csv_files = []
for directory in top_level_directories:
    csv_files.extend(find_csv_files(directory))

# Function to load a CSV file and align its columns
def load_and_align_csv(file):
    df = pd.read_csv(file, header=None)
    # Check if the first row contains non-numeric values (likely to be a header)
    if not pd.to_numeric(df.iloc[0], errors='coerce').notna().all():
        df.columns = df.iloc[0]  # Treat first row as header
        df = df.drop(0).reset_index(drop=True)
    df.columns = range(df.shape[1])  # Reassign numeric column names
    return df

# Load and align all the CSV files
dfs = [load_and_align_csv(file) for file in csv_files]

# Combine the dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Ensure the 'Time' column is numeric and the other columns are consistent
combined_df[0] = pd.to_numeric(combined_df[0], errors='coerce')
for col in combined_df.columns[1:]:
    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

# Sort by 'Time' to ensure proper alignment during groupby
combined_df = combined_df.sort_values(by=[0]).reset_index(drop=True)

# Compute the mean (assumes 'Time' is the first column)
mean_df = combined_df.groupby(0).mean().reset_index()

# Compute the standard deviation
std_df = combined_df.groupby(0).agg(lambda x: np.sqrt(np.mean((x - np.mean(x))**2))).reset_index()

# Rename the columns for clarity (assumes 'Time' is the first column)
mean_df.columns = [f'{col}_mean' if col != 0 else 'Time' for col in mean_df.columns]
std_df.columns = [f'{col}_std' if col != 0 else 'Time' for col in std_df.columns]

# Merge the mean and standard deviation into a single DataFrame
result_df = pd.merge(mean_df, std_df, on='Time')

# Save the combined dataframe to a new CSV file, if needed
result_df.to_csv('dummy_tests/combined_mean_std_results.csv', index=False)

# Display the result
print(result_df)
