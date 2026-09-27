#!/usr/bin/env pvpython
import csv, os, sys
from paraview.simple import *
from paraview import servermanager

if len(sys.argv) != 4:
    print("usage: {} <input_mesh> <output_csv> <block_name>".format(sys.argv[0]))
    sys.exit(1)

path_matrix, path_csv, block_input = sys.argv[1:4]
block_selector = block_input if block_input.startswith("/IOSS/") else "/IOSS/element_blocks/{}".format(block_input)
print("Fracture selector:", block_selector)

parent=os.path.dirname(os.path.abspath(path_csv))
if parent:
    os.makedirs(parent, exist_ok=True)

reader=IOSSReader(registrationName="matrix_transport.e", FileName=[path_matrix])
reader.UpdatePipeline()

try:
    times=list(reader.TimestepValues)
except Exception:
    times=[]
if not times:
    scene=GetAnimationScene()
    scene.UpdateAnimationUsingDataTimeSteps()
    times=list(reader.TimestepValues)
if not times:
    raise RuntimeError("No time steps found in {}".format(path_matrix))

fracture=ExtractBlock(registrationName="Extract_fracture", Input=reader)
fracture.Selectors=[block_selector]
fracture.UpdatePipeline(time=times[0])
if fracture.GetDataInformation().GetNumberOfCells() == 0:
    raise RuntimeError("Empty fracture selection: {}".format(block_selector))

integrated=IntegrateVariables(registrationName="Integrate_fracture", Input=fracture)

def leaves(obj):
    if obj.IsA("vtkCompositeDataSet"):
        it=obj.NewIterator()
        it.UnRegister(None)
        it.InitTraversal()
        while not it.IsDoneWithTraversal():
            child=it.GetCurrentDataObject()
            if child is not None:
                if child.IsA("vtkCompositeDataSet"):
                    for x in leaves(child):
                        yield x
                else:
                    yield child
            it.GoToNextItem()
    else:
        yield obj

def first(arr):
    if arr is None or arr.GetNumberOfTuples() == 0:
        return None
    return float(arr.GetComponent(0,0))

def integral_and_area(t):
    integrated.UpdatePipeline(time=t)
    obj=servermanager.Fetch(integrated)
    cint=0.0
    area=0.0
    have_c=False
    have_a=False
    for ds in leaves(obj):
        for attrs in (ds.GetPointData(), ds.GetCellData(), ds.GetFieldData()):
            if attrs is None:
                continue
            a=attrs.GetArray("concentration")
            if a is not None:
                v=first(a)
                if v is not None:
                    cint += v
                    have_c=True
            a=attrs.GetArray("Area")
            if a is not None:
                v=first(a)
                if v is not None:
                    area += v
                    have_a=True
    if not have_c:
        raise RuntimeError("Integrated 'concentration' array not found.")
    if not have_a or area <= 0:
        raise RuntimeError("Valid integrated 'Area' not found; verify that the selected block is a 2-D fracture.")
    return cint, area

reference_area=None
with open(path_csv, "w", newline="") as f:
    w=csv.writer(f)
    w.writerow(["Time", "mean(concentration)"])
    for k,t in enumerate(times):
        cint,area=integral_and_area(t)
        if reference_area is None:
            reference_area=area
        else:
            tol=max(1e-12,1e-9*abs(reference_area))
            if abs(area-reference_area)>tol:
                raise RuntimeError("Fracture area changed: {} -> {} at t={}".format(reference_area,area,t))
        mean_c=cint/area
        w.writerow(["{:.17g}".format(float(t)), "{:.17g}".format(float(mean_c))])
        if k == 0 or k == len(times)-1:
            print("t={:.17g} integral={:.17g} Area={:.17g} mean={:.17g}".format(float(t),cint,area,mean_c))
        if k == 0 or (k+1)%10 == 0 or k == len(times)-1:
            print("Processed {}/{} time steps".format(k+1,len(times)))

print("Area:", reference_area)
print("Output:", path_csv)
print("mean(concentration) = integral(concentration dA) / Area")
