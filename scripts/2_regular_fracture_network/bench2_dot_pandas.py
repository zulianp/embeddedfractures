#UNIRE CSV
import pandas as pd
import numpy as np
import sys

argv=sys.argv

if len(argv) < 5:
	print(f'usage: {argv[0]}  <input_csv1> <input_csv2> <input_csv3> <output_csv>')
	exit()

input_csv1=argv[1]
input_csv2=argv[2]
input_csv3=argv[3]

output_csv=argv[4]


df1=pd.read_csv(input_csv1)
df1=df1.to_numpy()

df1[:,1]=np.multiply(df1[:,1],8)
df1=pd.DataFrame(df1)

df1 = df1.rename(columns={df1.columns[0]: 'Time'})
df1 = df1.rename(columns={df1.columns[1]: 'concentration_block1' })



df2=pd.read_csv(input_csv2)
df2=df2.to_numpy()

df2[:,1]=np.multiply(df2[:,1],64)
df2=pd.DataFrame(df2)

df2 = df2.rename(columns={df2.columns[0]: 'Time'})
df2 = df2.rename(columns={df2.columns[1]: 'concentration_block10'})



df3=pd.read_csv(input_csv3)
df3=df3.to_numpy()

df3[:,1]=np.multiply(df3[:,1],64)
df3=pd.DataFrame(df3)

df3 = df3.rename(columns={df3.columns[0]: 'Time'})
df3 = df3.rename(columns={df3.columns[1]: 'concentration_block11'})



df=df1.set_index('Time').join(df2.set_index('Time')).join(df3.set_index('Time'))


df.to_csv(output_csv, columns=None, header=None)