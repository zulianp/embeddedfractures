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

# Load the CSV files into a list of dataframes
dfs = [pd.read_csv(file) for file in csv_files]

# Combine the dataframes
combined_df = pd.concat(dfs)

# Compute the mean
mean_df = combined_df.groupby('Time').mean().reset_index()

# Compute the standard deviation
std_df = combined_df.groupby('Time').agg(lambda x: np.sqrt(np.mean((x - np.mean(x))**2))).reset_index()

# Rename the columns for clarity
mean_df.columns = [f'{col}_mean' if col != 'Time' else 'Time' for col in mean_df.columns]
std_df.columns = [f'{col}_std' if col != 'Time' else 'Time' for col in std_df.columns]

# Merge the mean and standard deviation into a single DataFrame
result_df = pd.merge(mean_df, std_df, on='Time')

# Save the combined dataframe to a new CSV file, if needed
result_df.to_csv('combined_mean_std_results.csv', index=False)

# Display the result
print(result_df)
