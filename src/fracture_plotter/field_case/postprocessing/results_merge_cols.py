#UNIRE CSV
import pandas as pd
import numpy as np
import sys

argv=sys.argv

if len(argv) < 6:
	print(f'usage: {argv[0]}  <input_csv1> <input_csv2> <input_csv3> <input_csv4> <output_csv>')
	exit()

input_csv1=argv[1]
input_csv2=argv[2]
input_csv3=argv[3]
input_csv4=argv[4]

output_csv=argv[5]


df1=pd.read_csv(input_csv1)

df2=pd.read_csv(input_csv2)
df2 = df2.rename(columns={df2.columns[0]: '6' })

df3=pd.read_csv(input_csv3)
df3 = df3.rename(columns={df3.columns[0]: '7' })

df4=pd.read_csv(input_csv4)
df4 = df4.rename(columns={df4.columns[0]: '8' })




df=df1.join(df2).join(df3).join(df4)
 

df.to_csv(output_csv, columns=None, header= None)