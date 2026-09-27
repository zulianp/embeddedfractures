#!/usr/bin/env pvpython
# ParaView 5.12.x
#
# Usage:
#   pvpython bench2_dot_blockid1_10_11.py \
#       <matrix_transport.e> \
#       <csv_Omega31> <csv_Omega32> <csv_Omega33>
#
# Computes, for each matrix region Omega_3,i and every transport time:
#
#        avg(c)_i = integral_{Omega_3,i} c dV / |Omega_3,i|
#
# The geometric regions reproduce the Clip sequence recorded in the
# original ParaView trace. Origins that were NOT explicitly modified in
# that trace are intentionally left at ParaView's automatically initialized
# value.

import sys
import os
import csv
import math

from paraview.simple import IOSSReader, Clip, IntegrateVariables
from paraview.simple import UpdatePipeline
from paraview import servermanager


# ----------------------------------------------------------------------
# Arguments
# ----------------------------------------------------------------------
argv = sys.argv

if len(argv) != 5:
    print(
        "usage: {} <input_mesh> <output_csv1> <output_csv2> <output_csv3>"
        .format(argv[0])
    )
    sys.exit(1)

path_matrix = argv[1]
path_csv1 = argv[2]
path_csv2 = argv[3]
path_csv3 = argv[4]

output_paths = [path_csv1, path_csv2, path_csv3]

print("Transport:", path_matrix)
print("Outputs:")
for p in output_paths:
    print("  ", p)

for p in output_paths:
    parent = os.path.dirname(os.path.abspath(p))
    if parent:
        os.makedirs(parent, exist_ok=True)


# ----------------------------------------------------------------------
# Reader
# ----------------------------------------------------------------------
reader = IOSSReader(
    registrationName="matrix_transport.e",
    FileName=[path_matrix],
)

# Request only the quantity needed when the properties are available.
try:
    reader.PointArrays = ["concentration"]
except Exception:
    pass

# Side sets are not part of the matrix-volume average.
try:
    reader.SideSets = []
except Exception:
    pass

reader.UpdatePipelineInformation()

times = []

try:
    times = list(reader.TimestepValues)
except Exception:
    pass

if not times:
    try:
        scene_times = reader.GetProperty("TimestepValues")
        if scene_times is not None:
            times = list(scene_times)
    except Exception:
        pass

if not times:
    raise RuntimeError("No transport time steps found in matrix_transport.e")

print("Transport time steps:", len(times))
print("First time:", times[0])
print("Last time :", times[-1])

# Initialize the data pipeline at the first actual transport time.
UpdatePipeline(time=times[0], proxy=reader)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def make_clip(name, input_proxy, normal, origin=None):
    """
    Create a Plane Clip.

    If origin is None, DO NOT assign ClipType.Origin. This is deliberate:
    the original GUI trace did not modify that origin, so ParaView must
    initialize it from the current input bounds.
    """
    c = Clip(registrationName=name, Input=input_proxy)

    # Plane is the default Clip type in the recorded ParaView trace.
    if origin is not None:
        c.ClipType.Origin = list(origin)

    c.ClipType.Normal = list(normal)

    # Do not set Invert / InsideOut. The original trace did not change it.
    UpdatePipeline(time=times[0], proxy=c)
    return c


def data_arrays(proxy, t):
    UpdatePipeline(time=t, proxy=proxy)
    info = proxy.GetDataInformation()

    point_names = []
    cell_names = []

    pdi = info.GetPointDataInformation()
    cdi = info.GetCellDataInformation()

    for i in range(pdi.GetNumberOfArrays()):
        ai = pdi.GetArrayInformation(i)
        if ai is not None:
            point_names.append(ai.GetName())

    for i in range(cdi.GetNumberOfArrays()):
        ai = cdi.GetArrayInformation(i)
        if ai is not None:
            cell_names.append(ai.GetName())

    return point_names, cell_names


def fetch_integral(integrator, t):
    """
    Return (integral_concentration, volume).

    IntegrateVariables produces a one-point output. For volumetric input,
    Volume is normally stored in CellData while integrated point fields
    such as concentration are normally in PointData.
    """
    UpdatePipeline(time=t, proxy=integrator)
    obj = servermanager.Fetch(integrator)

    if obj is None:
        raise RuntimeError("servermanager.Fetch returned no data")

    # Composite output is possible with IOSS pipelines. IntegrateVariables
    # normally reduces it, but handle both simple and composite datasets.
    datasets = []

    if hasattr(obj, "NewIterator"):
        it = obj.NewIterator()
        it.UnRegister(None)
        it.InitTraversal()
        while not it.IsDoneWithTraversal():
            block = it.GetCurrentDataObject()
            if block is not None:
                datasets.append(block)
            it.GoToNextItem()
    else:
        datasets = [obj]

    cint = 0.0
    volume = 0.0
    found_c = False
    found_v = False

    for ds in datasets:
        pd = ds.GetPointData() if hasattr(ds, "GetPointData") else None
        cd = ds.GetCellData() if hasattr(ds, "GetCellData") else None
        fd = ds.GetFieldData() if hasattr(ds, "GetFieldData") else None

        # Integrated concentration can appear in PointData, CellData,
        # or FieldData depending on the input association/version.
        carr = None
        for attrs in (pd, cd, fd):
            if attrs is not None:
                a = attrs.GetArray("concentration")
                if a is not None and a.GetNumberOfTuples() > 0:
                    carr = a
                    break

        if carr is not None:
            cint += float(carr.GetTuple1(0))
            found_c = True

        # IntegrateVariables normally stores Volume in CellData.
        varr = None
        for attrs in (cd, pd, fd):
            if attrs is not None:
                a = attrs.GetArray("Volume")
                if a is not None and a.GetNumberOfTuples() > 0:
                    varr = a
                    break

        if varr is not None:
            volume += float(varr.GetTuple1(0))
            found_v = True

    if not found_c:
        raise RuntimeError(
            "Integrated array 'concentration' is missing at time {}".format(t)
        )

    if not found_v:
        raise RuntimeError(
            "Integrated array 'Volume' is missing at time {}".format(t)
        )

    if not math.isfinite(volume) or volume <= 0.0:
        raise RuntimeError(
            "Invalid/zero matrix-region volume {} at time {}".format(volume, t)
        )

    return cint, volume


# ----------------------------------------------------------------------
# Omega_3,1
#
# Trace:
#   clip1 Normal = [-1, 0, 0]
#   clip2 Normal = [ 0, 1, 0]
#   clip3 Normal = [ 0, 0, 1]
#
# No explicit Origin was recorded for these clips.
# ----------------------------------------------------------------------
c1 = make_clip("Omega31_Clip1", reader, [-1.0, 0.0, 0.0])
c2 = make_clip("Omega31_Clip2", c1,     [ 0.0, 1.0, 0.0])
omega31 = make_clip("Omega31_Clip3", c2, [0.0, 0.0, 1.0])


# ----------------------------------------------------------------------
# Omega_3,2
#
# Final effective values in the trace:
#   clip4: Normal = [-1,0,0], Origin untouched
#   clip5: Normal = [ 1,0,0], Origin untouched
#   clip6: Origin = [0.5,0.5,0.5],   Normal = [0,-1,0]
#   clip7: Origin = [0.5,0.75,0.5],  Normal = [0, 1,0]
#   clip8: Origin = [0.625,0.625,0.75], Normal = [0,0,-1]
# ----------------------------------------------------------------------
c4 = make_clip("Omega32_Clip4", reader, [-1.0, 0.0, 0.0])
c5 = make_clip("Omega32_Clip5", c4,     [ 1.0, 0.0, 0.0])
c6 = make_clip(
    "Omega32_Clip6", c5,
    [0.0, -1.0, 0.0],
    origin=[0.5, 0.5, 0.5],
)
c7 = make_clip(
    "Omega32_Clip7", c6,
    [0.0, 1.0, 0.0],
    origin=[0.5, 0.75, 0.5],
)
omega32 = make_clip(
    "Omega32_Clip8", c7,
    [0.0, 0.0, -1.0],
    origin=[0.625, 0.625, 0.75],
)


# ----------------------------------------------------------------------
# Omega_3,3
#
# Trace:
#   clip9 : Origin = [0.75,0.5,0.5],   Normal = [-1,0,0]
#   clip10: Origin = [0.875,0.75,0.5], Normal = [0,-1,0]
#   clip11: Origin untouched, Normal = [0,0,-1]
#   clip12: Origin untouched, Normal = [0,0, 1]
# ----------------------------------------------------------------------
c9 = make_clip(
    "Omega33_Clip9", reader,
    [-1.0, 0.0, 0.0],
    origin=[0.75, 0.5, 0.5],
)
c10 = make_clip(
    "Omega33_Clip10", c9,
    [0.0, -1.0, 0.0],
    origin=[0.875, 0.75, 0.5],
)
c11 = make_clip("Omega33_Clip11", c10, [0.0, 0.0, -1.0])
omega33 = make_clip("Omega33_Clip12", c11, [0.0, 0.0, 1.0])


regions = [omega31, omega32, omega33]

# ----------------------------------------------------------------------
# Validate region outputs before processing all times.
# ----------------------------------------------------------------------
for i, region in enumerate(regions, start=1):
    pnames, cnames = data_arrays(region, times[0])

    print("Omega_3,{}:".format(i))
    print("  Point Data:", pnames)
    print("  Cell Data :", cnames)

    if "concentration" not in pnames and "concentration" not in cnames:
        raise RuntimeError(
            "concentration missing from Omega_3,{}; "
            "the geometric region is empty or the Clip sequence is incorrect"
            .format(i)
        )


# ----------------------------------------------------------------------
# Integrate each region.
# ----------------------------------------------------------------------
integrators = [
    IntegrateVariables(registrationName="Integrate_Omega31", Input=omega31),
    IntegrateVariables(registrationName="Integrate_Omega32", Input=omega32),
    IntegrateVariables(registrationName="Integrate_Omega33", Input=omega33),
]

for integ in integrators:
    UpdatePipeline(time=times[0], proxy=integ)


# ----------------------------------------------------------------------
# Open all output CSVs immediately.
#
# This deliberately avoids PlotDataOverTime. We explicitly visit every
# transport timestep and compute the volume-normalized integral.
# ----------------------------------------------------------------------
files = []
writers = []

try:
    for path in output_paths:
        f = open(path, "w", newline="")
        files.append(f)

        w = csv.writer(f)
        w.writerow(["Time", "avg(concentration)"])
        writers.append(w)

    reference_volumes = [None, None, None]

    for k, t in enumerate(times):
        # Update source first, then each integration pipeline.
        UpdatePipeline(time=t, proxy=reader)

        for i, integ in enumerate(integrators):
            cint, volume = fetch_integral(integ, t)
            avg = cint / volume

            if not math.isfinite(avg):
                raise RuntimeError(
                    "Non-finite average concentration in Omega_3,{} at time {}"
                    .format(i + 1, t)
                )

            if reference_volumes[i] is None:
                reference_volumes[i] = volume

            writers[i].writerow([
                "{:.17g}".format(float(t)),
                "{:.17g}".format(float(avg)),
            ])

        # Flush periodically so a partial CSV remains available if a later
        # timestep fails.
        if k == 0 or (k + 1) % 10 == 0 or k == len(times) - 1:
            for f in files:
                f.flush()
            print("Processed time step {}/{}: {}".format(k + 1, len(times), t))

finally:
    for f in files:
        try:
            f.close()
        except Exception:
            pass


# ----------------------------------------------------------------------
# Final validation
# ----------------------------------------------------------------------
print("")
for i, (path, volume) in enumerate(zip(output_paths, reference_volumes), start=1):
    print("Omega_3,{} validation".format(i))
    print("  volume:", volume)
    print("  csv   :", path)

    if not os.path.isfile(path):
        raise RuntimeError("Output CSV was not created: {}".format(path))

    if os.path.getsize(path) == 0:
        raise RuntimeError("Output CSV is empty: {}".format(path))

print("")
print("Done. All three CSV files were written successfully.")
