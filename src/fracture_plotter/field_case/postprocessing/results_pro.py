import meshio
import sys
import pdb
import pandas as pd

m=meshio.read(sys.argv[1])
n=meshio.read(sys.argv[2])
output_csv=sys.argv[3]
cells3D=0
cells2D=0

for b in m.cells:
	cells2D=b.data.shape[0] + cells2D

for b in n.cells:
    cells3D= b.data.shape[0] + cells3D


points3D=n.points.shape[0]
nnz = 0



df=[ 0,0, cells2D, cells3D, points3D, nnz]
df = pd.DataFrame(df)
df.transpose().to_csv(output_csv, index=False)

	#pdb.set_trace() #,