#SCALE BY AREA
import pandas as pd
import numpy as np
import sys

argv=sys.argv

if len(argv) < 4:
	print(f'usage: {argv[0]}  <input_csv1> <input_csv2> <output_csv> ')
	exit()

input_csv1=argv[1]
input_csv2=argv[2]
output_csv=argv[3]


df1=pd.read_csv(input_csv1)
df2=pd.read_csv(input_csv2)
print (df1)
df2=df2["Area"]
df2=df2.to_numpy()
print (df2)
df1["avg(concentration)"]=df1["avg(concentration)"]/df2
print(df1)



df1.to_csv(output_csv, index=False, header=True)