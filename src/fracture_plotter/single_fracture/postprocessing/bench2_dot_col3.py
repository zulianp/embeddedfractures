# Benchmark 1 - outlet concentration flux
# ParaView 5.12.x - version avoiding ResampleWithDataset on composite IOSS data.
#
# SAME INTERFACE AS THE ORIGINAL SCRIPT:
#   pvpython bench2_dot_col3.py <matrix_transport.e> <output_csv>
#
# matrix_flow.e is searched automatically beside matrix_transport.e.

import os
import sys
from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

if len(sys.argv) < 3:
    print(f"usage: {sys.argv[0]} <matrix_transport.e> <output_csv>")
    sys.exit(1)

path_transport = os.path.abspath(sys.argv[1])

# Absolute output path shared by pvpython and the following pandas step.
path_csv = os.path.abspath(sys.argv[2])
output_dir = os.path.dirname(path_csv)
os.makedirs(output_dir, exist_ok=True)

case_dir = os.path.dirname(path_transport)
path_flow = os.path.join(case_dir, "matrix_flow.e")

if not os.path.isfile(path_flow):
    raise FileNotFoundError(
        "matrix_flow.e not found beside matrix_transport.e:\n" + path_flow
    )

# ------------------------------------------------------------------
# Physical/model settings
# ------------------------------------------------------------------
# Benchmark 1: the outlet is z in (0,10 m), i.e. the bottom
# heterogeneous matrix layer Omega_3,3.  Table 3 gives
# K_3,3 = 1e-5 m/s.  The Exodus variable 'pressure' is hydraulic
# head h [m], so Darcy's law is q = -K grad(h), with NO viscosity factor.
K_OUTLET = 1.0e-5
MATRIX_BLOCK = "block_2"
OUTLET_SIDESET = "surface_1"

print("Transport:", path_transport)
print("Flow     :", path_flow)
print("Output   :", path_csv)

# ------------------------------------------------------------------
# Transport volume: concentration
# MergeBlocks converts the IOSS composite output to a simple dataset.
# This is important for stability with ParaView 5.12.x.
# ------------------------------------------------------------------
transport_reader = IOSSReader(
    registrationName="matrix_transport_volume",
    FileName=[path_transport]
)
transport_reader.ElementBlocks = [MATRIX_BLOCK]
transport_reader.SideSets = []

transport = MergeBlocks(
    registrationName="transport_volume",
    Input=transport_reader
)
transport.MergePoints = 1

# ------------------------------------------------------------------
# Flow volume: hydraulic head -> grad(h) -> Darcy velocity
# ------------------------------------------------------------------
flow_reader = IOSSReader(
    registrationName="matrix_flow_volume",
    FileName=[path_flow]
)
flow_reader.ElementBlocks = [MATRIX_BLOCK]
flow_reader.SideSets = []

flow = MergeBlocks(
    registrationName="flow_volume",
    Input=flow_reader
)
flow.MergePoints = 1

grad_p = Gradient(
    registrationName="pressure_gradient",
    Input=flow
)
grad_p.ScalarArray = ["POINTS", "pressure"]
grad_p.ResultArrayName = "grad_pressure"

darcy = Calculator(
    registrationName="darcy_velocity",
    Input=grad_p
)
darcy.ResultArrayName = "darcy_velocity"
darcy.Function = "-(" + str(K_OUTLET) + ")*grad_pressure"

# ------------------------------------------------------------------
# Put the steady Darcy field on the transport volume.
# Both inputs are now ordinary merged datasets rather than IOSS
# composite datasets.
# ------------------------------------------------------------------
volume_fields = ResampleWithDataset(
    registrationName="transport_plus_darcy",
    SourceDataArrays=darcy,
    DestinationMesh=transport
)

# Preserve arrays already present on the destination mesh (notably concentration).
# ParaView versions expose these properties on ResampleWithDataset.
if hasattr(volume_fields, 'PassPointArrays'):
    volume_fields.PassPointArrays = 1
if hasattr(volume_fields, 'PassCellArrays'):
    volume_fields.PassCellArrays = 1

# ------------------------------------------------------------------
# Outlet geometry from the transport Exodus file.
# ------------------------------------------------------------------
outlet_reader = IOSSReader(
    registrationName="matrix_transport_outlet",
    FileName=[path_transport]
)
outlet_reader.ElementBlocks = []
outlet_reader.SideSets = [OUTLET_SIDESET]

outlet = MergeBlocks(
    registrationName="outlet_surface",
    Input=outlet_reader
)
outlet.MergePoints = 1

# Sample concentration + q onto the simple 2-D outlet dataset.
outlet_fields = ResampleWithDataset(
    registrationName="fields_on_outlet",
    SourceDataArrays=volume_fields,
    DestinationMesh=outlet
)

# Keep destination arrays as well.
if hasattr(outlet_fields, 'PassPointArrays'):
    outlet_fields.PassPointArrays = 1
if hasattr(outlet_fields, 'PassCellArrays'):
    outlet_fields.PassCellArrays = 1

outlet_fields.UpdatePipeline()

# Fail early if concentration was not propagated to the outlet.
_out_pd = outlet_fields.GetPointDataInformation()
_out_cd = outlet_fields.GetCellDataInformation()
_out_pnames = [_out_pd.GetArray(i).GetName() for i in range(_out_pd.GetNumberOfArrays())]
_out_cnames = [_out_cd.GetArray(i).GetName() for i in range(_out_cd.GetNumberOfArrays())]
print("Outlet Point Data:", _out_pnames)
print("Outlet Cell Data :", _out_cnames)

if 'concentration' not in _out_pnames and 'concentration' not in _out_cnames:
    raise RuntimeError(
        "concentration was not transferred to the outlet. "
        "Point Data=" + str(_out_pnames) + "; Cell Data=" + str(_out_cnames)
    )

# ------------------------------------------------------------------
# Convert the outlet from vtkUnstructuredGrid to vtkPolyData.
# GenerateSurfaceNormals requires vtkPolyData in ParaView 5.12.1.
# ------------------------------------------------------------------
outlet_polydata = ExtractSurface(
    registrationName="outlet_polydata",
    Input=outlet_fields
)

# ------------------------------------------------------------------
# Surface normal, q.n and concentration flux.
# ------------------------------------------------------------------
normals = GenerateSurfaceNormals(
    registrationName="outlet_normals",
    Input=outlet_polydata
)

qn = Calculator(
    registrationName="normal_darcy_flux",
    Input=normals
)
qn.ResultArrayName = "normal_darcy_flux"
qn.Function = "dot(darcy_velocity,Normals)"

cq = Calculator(
    registrationName="concentration_flux_density",
    Input=qn
)
cq.ResultArrayName = "concentration_flux"
cq.Function = "concentration*normal_darcy_flux"

# Surface integral at every transport time.
integrated = IntegrateVariables(
    registrationName="integrated_outlet_flux",
    Input=cq
)

# ------------------------------------------------------------------
# EXPLICIT TRANSPORT TIME LOOP
#
# matrix_flow.e is steady (one time step), while matrix_transport.e
# contains the transient concentration.  PlotDataOverTime on the
# combined pipeline can collapse to the single flow time.  Therefore
# we explicitly iterate over the transport reader time steps.
# ------------------------------------------------------------------
transport_reader.UpdatePipelineInformation()

time_values = []

# ParaView readers normally expose TimestepValues.
if hasattr(transport_reader, "TimestepValues"):
    try:
        time_values = list(transport_reader.TimestepValues)
    except Exception:
        time_values = []

# Fallback through data information if needed.
if not time_values:
    try:
        time_values = list(
            transport_reader.GetDataInformation().GetTimeSteps()
        )
    except Exception:
        time_values = []

if not time_values:
    raise RuntimeError(
        "No transport time steps were found in matrix_transport.e"
    )

print("Transport time steps found:", len(time_values))
print("First transport time:", time_values[0])
print("Last transport time :", time_values[-1])

# Use VTK's server-manager fetch to read the single integrated value.
from paraview import servermanager

rows = []

for i, t in enumerate(time_values):
    # Update every time-dependent branch at the requested transport time.
    transport_reader.UpdatePipeline(t)
    transport.UpdatePipeline(t)
    volume_fields.UpdatePipeline(t)
    outlet_reader.UpdatePipeline(t)
    outlet.UpdatePipeline(t)
    outlet_fields.UpdatePipeline(t)
    outlet_polydata.UpdatePipeline(t)
    normals.UpdatePipeline(t)
    qn.UpdatePipeline(t)
    cq.UpdatePipeline(t)
    integrated.UpdatePipeline(t)

    data = servermanager.Fetch(integrated)

    value = None

    # IntegrateVariables may place the integrated array in point data
    # or cell data depending on the input association.
    for attrs in (data.GetPointData(), data.GetCellData()):
        if attrs is None:
            continue
        arr = attrs.GetArray("concentration_flux")
        if arr is not None and arr.GetNumberOfTuples() > 0:
            value = arr.GetTuple1(0)
            break

    if value is None:
        # Diagnostic: show all arrays if the expected one is missing.
        available = []
        for label, attrs in (
            ("PointData", data.GetPointData()),
            ("CellData", data.GetCellData()),
            ("FieldData", data.GetFieldData()),
        ):
            if attrs is not None:
                for j in range(attrs.GetNumberOfArrays()):
                    a = attrs.GetArray(j)
                    if a is not None:
                        available.append(label + ":" + a.GetName())
        raise RuntimeError(
            "Integrated concentration_flux not found at time "
            + str(t) + ". Available arrays: " + str(available)
        )

    rows.append((float(t), float(value)))

    if i == 0 or i == len(time_values) - 1 or (i + 1) % 10 == 0:
        print(
            "time step", i + 1, "/", len(time_values),
            "t =", t,
            "integrated concentration flux =", value
        )

# ------------------------------------------------------------------
# WRITE CSV DIRECTLY
#
# This avoids PlotDataOverTime collapsing the transient history to the
# single steady-flow time step.
# ------------------------------------------------------------------
import csv

with open(path_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "avg(concentration_flux)"])
    writer.writerows(rows)

if not os.path.isfile(path_csv):
    raise RuntimeError(
        "The expected CSV was not created: " + path_csv
    )

print("")
print("Outlet flux CSV written:", path_csv)
print("Number of rows:", len(rows))
