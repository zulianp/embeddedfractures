#UNIRE CSV
import pandas as pd
import numpy as np
import sys

argv=sys.argv

if len(argv) < 5:
	print(f'usage: {argv[0]}  <input_csv1> <input_csv2> <output_csv> <block_number> ')
	exit()

input_csv1=argv[1]
input_csv2=argv[2]
output_csv=argv[3]
block = argv[4]
block = int(block)



df1=pd.read_csv(input_csv1)
df2=pd.read_csv(input_csv2)
df2 = df2.rename(columns={df2.columns[1]: 'concentration_block%s' %(block) } )
df=df1.set_index('Time').join(df2.set_index('Time'))

df.columns = range(0, block, 1)


first_row= [0] * (block)
first_row=(first_row)


dff = pd.DataFrame([first_row])

df = pd.concat([dff, df], ignore_index=False)

df.to_csv(output_csv, header=None)