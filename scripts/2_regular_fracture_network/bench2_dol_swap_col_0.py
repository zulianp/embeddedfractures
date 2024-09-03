import pandas as pd
import sys

argv=sys.argv

if len(argv) < 4:
	print(f'usage: {argv[0]} <input_csv> <output_csv> <index> <refinment>')
	exit()

path_matrix=argv[1]
path_csv=argv[2]
refinment=argv[3]
print(refinment)

#create DataFrame
df = pd.read_csv(path_matrix)

#view DataFrame
#define function to swap columns
def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

#swap points and rebounds columns
df = swap_columns(df, 'pressure', 'arc_length')
df.to_csv(path_csv, index=False, header=None)
#view updated DataFrame
print(df)