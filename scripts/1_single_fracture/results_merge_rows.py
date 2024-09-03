import pandas as pd
import numpy
import sys

argv=sys.argv

if len(argv) < 4:
	print(f'usage: {argv[0]}   <output_csv> <refs> <PWD>')
	exit()

output_csv=argv[1]
tot_ref=argv[2]
here=argv[3]
print('scritp 2')
print('%s' %tot_ref)

tot_ref=int(tot_ref)
df = [ [ 0 for j in range(6) ] for k in range(tot_ref) ] 

for i in range(0,tot_ref):
	print("%s/results_cond1_ref%d.csv" %(here,i) )
	df_i= pd.read_csv("%s/results_cond1_ref%d.csv" %(here,i) ) 
	df_i=df_i.loc[0]
	df[i]= df_i
	print(df)


df_output = pd.DataFrame(df)
df_output.to_csv(output_csv, index=False, header=None)
