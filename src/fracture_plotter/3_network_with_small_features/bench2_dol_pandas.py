#UNIRE CSV
import pandas as pd
import numpy as np
import sys

argv=sys.argv

if len(argv) < 4:
	print(f'usage: {argv[0]}  <input_csv1> <input_csv2> <output_csv>')
	exit()

input_csv1=argv[1]
input_csv2=argv[2]
output_csv=argv[3]


df1=pd.read_csv(input_csv1)
df1 = df1.rename(columns={df1.columns[1]: 'col1' })
df2=pd.read_csv(input_csv2)
df2 = df2.rename(columns={df2.columns[1]: 'col2'})

df=df1.set_index('arc_length').join(df2.set_index('arc_length'))


df.to_csv(output_csv, columns=None)