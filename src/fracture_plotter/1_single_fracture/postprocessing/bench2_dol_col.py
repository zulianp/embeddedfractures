import pandas as pd
import sys

argv=sys.argv

if len(argv) < 6:
	print(f'usage: {argv[0]} <input_csv1> <input_csv2> <input_csv3> <output_csv> <index> <refinment>')
	exit()

input_csv1=argv[1]
input_csv2=argv[2]
input_csv3=argv[3]

path_csv=argv[4]
refinment=argv[5]
print(refinment)

#create DataFrame
df = pd.read_csv(input_csv1)

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



df3 = pd.read_csv(input_csv3)
df3 = swap_columns(df3, 'concentration', 'arc_length')

df2 = pd.read_csv(input_csv2)
df2 = swap_columns(df2, 'concentration', 'arc_length')



# Add the new column using loc
#df.loc[:, "c3"] = df2
#df.loc[:, "c2"] = df3

dff = pd.concat([df, df2, df3], axis=1, ignore_index='True')




dff.to_csv(path_csv, index=False, header=None)
#view updated DataFrame
print(dff)

