#!/usr/bin/env pvpython
"""
Regular fracture benchmark — Case 2
Average matrix concentration for paper region IDs 1, 10 and 11.

Paper:
  Berre et al., arXiv:1809.06926
  Appendix 6.1 region definitions.

Usage (compatible with existing DOT.sh):
  pvpython bench2_dot_blockid1_10_11.py \
      matrix_transport.e \
      dot_cond1_block1.csv \
      dot_cond1_block10.csv \
      dot_cond1_block11.csv

Output CSV format is intentionally kept compatible with the existing
bench2_dot_pandas.py:
    Time,avg(concentration)

Definition:
    avg(c3) = integral_{Omega_3,i} c3 dV / |Omega_3,i|

Paper regions:
  region 1:
      x > 0.5, y < 0.5, z < 0.5
      expected volume = 0.5^3 = 0.125

  region 10:
      0.5 < x < 0.75,
      0.5 < y < 0.75,
      z > 0.75
      expected volume = 0.25^3 = 0.015625

  region 11:
      x > 0.75,
      y > 0.75,
      0.5 < z < 0.75
      expected volume = 0.25^3 = 0.015625
"""

from paraview.simple import *
from paraview import servermanager
import csv
import os
import sys
import math


# ----------------------------------------------------------------------
# Command line
# ----------------------------------------------------------------------

if len(sys.argv) != 5:
    raise RuntimeError(
        "Usage: pvpython {} matrix_transport.e out_region1.csv "
        "out_region10.csv out_region11.csv".format(sys.argv[0])
    )

path_matrix = sys.argv[1]
output_paths = [sys.argv[2], sys.argv[3], sys.argv[4]]

for p in output_paths:
    parent = os.path.dirname(os.path.abspath(p))
    if parent:
        os.makedirs(parent, exist_ok=True)


# ----------------------------------------------------------------------
# Reader
# ----------------------------------------------------------------------

matrix = IOSSReader(
    registrationName="matrix_transport.e",
    FileName=[path_matrix],
)

# Request concentration when the reader exposes PointArrays.
try:
    point_arrays = list(matrix.PointArrays)
    if "concentration" in point_arrays:
        matrix.PointArrays = ["concentration"]
except Exception:
    pass

# We only need the 3-D matrix data, not side sets.
try:
    matrix.SideSets = []
except Exception:
    pass

matrix.UpdatePipeline()

time_values = []
try:
    time_values = list(matrix.TimestepValues)
except Exception:
    pass

if not time_values:
    scene = GetAnimationScene()
    scene.UpdateAnimationUsingDataTimeSteps()
    try:
        time_values = list(matrix.TimestepValues)
    except Exception:
        time_values = []

if not time_values:
    raise RuntimeError("No transport time steps found in {}".format(path_matrix))

print("Transport time steps:", len(time_values))
print("First time:", time_values[0])
print("Last time :", time_values[-1])


# ----------------------------------------------------------------------
# Clip helpers
#
# ParaView's Clip side is made explicit by checking the resulting bounds.
# We use axis-aligned planes and, when necessary, flip Invert so that the
# requested inequality is satisfied. This removes dependence on GUI
# defaults.
# ----------------------------------------------------------------------

AXIS = {"x": 0, "y": 1, "z": 2}


def bounds_of(proxy, t=None):
    if t is None:
        proxy.UpdatePipeline()
    else:
        proxy.UpdatePipeline(time=t)
    b = proxy.GetDataInformation().GetBounds()
    return tuple(float(v) for v in b)


def make_halfspace(inp, axis, value, keep, name):
    """
    keep:
      'gt' -> coordinate > value
      'lt' -> coordinate < value

    We first create a +axis plane. Then inspect bounds and flip Invert if
    the retained side is not the requested one.
    """
    normal = [0.0, 0.0, 0.0]
    normal[AXIS[axis]] = 1.0

    origin = [0.5, 0.5, 0.5]
    origin[AXIS[axis]] = float(value)

    clip = Clip(registrationName=name, Input=inp)
    clip.ClipType = "Plane"
    clip.ClipType.Origin = origin
    clip.ClipType.Normal = normal

    # Test current side.
    clip.UpdatePipeline()
    b = bounds_of(clip)
    j = 2 * AXIS[axis]
    lo, hi = b[j], b[j + 1]

    tol = 1.0e-9
    good = False
    if keep == "gt":
        good = lo >= value - tol
    elif keep == "lt":
        good = hi <= value + tol
    else:
        raise ValueError("keep must be 'gt' or 'lt'")

    if not good:
        try:
            clip.Invert = 0 if int(clip.Invert) else 1
        except Exception:
            # Older ParaView versions can expose the same property under
            # InsideOut.
            if hasattr(clip, "InsideOut"):
                clip.InsideOut = 0 if int(clip.InsideOut) else 1
            else:
                raise RuntimeError(
                    "Cannot flip Clip side for {} {} {}".format(axis, keep, value)
                )
        clip.UpdatePipeline()

    # Strict final check.
    b = bounds_of(clip)
    lo, hi = b[j], b[j + 1]
    if keep == "gt" and lo < value - 1.0e-8:
        raise RuntimeError(
            "{} failed: expected {} > {}, bounds={}".format(name, axis, value, b)
        )
    if keep == "lt" and hi > value + 1.0e-8:
        raise RuntimeError(
            "{} failed: expected {} < {}, bounds={}".format(name, axis, value, b)
        )

    return clip


# ----------------------------------------------------------------------
# Region ID 1 — Appendix 6.1:
# x > 0.5, y < 0.5, z < 0.5
# ----------------------------------------------------------------------

r1 = make_halfspace(matrix, "x", 0.5, "gt", "region1_x_gt_05")
r1 = make_halfspace(r1,     "y", 0.5, "lt", "region1_y_lt_05")
r1 = make_halfspace(r1,     "z", 0.5, "lt", "region1_z_lt_05")


# ----------------------------------------------------------------------
# Region ID 10 — Appendix 6.1:
# 0.5 < x < 0.75, 0.5 < y < 0.75, z > 0.75
# ----------------------------------------------------------------------

r10 = make_halfspace(matrix, "x", 0.5,  "gt", "region10_x_gt_05")
r10 = make_halfspace(r10,    "x", 0.75, "lt", "region10_x_lt_075")
r10 = make_halfspace(r10,    "y", 0.5,  "gt", "region10_y_gt_05")
r10 = make_halfspace(r10,    "y", 0.75, "lt", "region10_y_lt_075")
r10 = make_halfspace(r10,    "z", 0.75, "gt", "region10_z_gt_075")


# ----------------------------------------------------------------------
# Region ID 11 — Appendix 6.1:
# x > 0.75, y > 0.75, 0.5 < z < 0.75
# ----------------------------------------------------------------------

r11 = make_halfspace(matrix, "x", 0.75, "gt", "region11_x_gt_075")
r11 = make_halfspace(r11,    "y", 0.75, "gt", "region11_y_gt_075")
r11 = make_halfspace(r11,    "z", 0.5,  "gt", "region11_z_gt_05")
r11 = make_halfspace(r11,    "z", 0.75, "lt", "region11_z_lt_075")


regions = [r1, r10, r11]
region_ids = [1, 10, 11]
expected_volumes = [0.125, 0.015625, 0.015625]


# ----------------------------------------------------------------------
# IntegrateVariables
# ----------------------------------------------------------------------

integrators = []
for rid, region in zip(region_ids, regions):
    integ = IntegrateVariables(
        registrationName="Integrate_region_{}".format(rid),
        Input=region,
    )
    integrators.append(integ)


def iter_leaf_datasets(obj):
    """Yield VTK leaf datasets from a fetched object."""
    if obj is None:
        return

    if obj.IsA("vtkCompositeDataSet"):
        it = obj.NewIterator()
        it.UnRegister(None)
        it.InitTraversal()
        while not it.IsDoneWithTraversal():
            child = it.GetCurrentDataObject()
            if child is not None:
                if child.IsA("vtkCompositeDataSet"):
                    for leaf in iter_leaf_datasets(child):
                        yield leaf
                else:
                    yield child
            it.GoToNextItem()
    else:
        yield obj


def first_component(array):
    if array is None or array.GetNumberOfTuples() == 0:
        return None
    return float(array.GetComponent(0, 0))


def extract_integral_and_volume(fetched):
    """
    IntegrateVariables normally stores integrated concentration in point
    data and Volume in cell data. Search both associations so the script
    is robust to ParaView/VTK representation details.
    """
    total_c = 0.0
    total_v = 0.0
    found_c = False
    found_v = False

    for ds in iter_leaf_datasets(fetched):
        for data in (ds.GetPointData(), ds.GetCellData(), ds.GetFieldData()):
            if data is None:
                continue

            arr_c = data.GetArray("concentration")
            if arr_c is not None:
                val = first_component(arr_c)
                if val is not None:
                    total_c += val
                    found_c = True

            arr_v = data.GetArray("Volume")
            if arr_v is not None:
                val = first_component(arr_v)
                if val is not None:
                    total_v += val
                    found_v = True

    if not found_c:
        raise RuntimeError(
            "Integrated array 'concentration' was not found. "
            "Check the array name in matrix_transport.e."
        )

    if not found_v:
        raise RuntimeError(
            "IntegrateVariables did not produce a 'Volume' array."
        )

    return total_c, total_v


# ----------------------------------------------------------------------
# Geometry validation
# ----------------------------------------------------------------------

print("")
print("Paper-region geometry validation")

for rid, region, integ, expected in zip(
    region_ids, regions, integrators, expected_volumes
):
    b = bounds_of(region, time_values[0])
    integ.UpdatePipeline(time=time_values[0])
    fetched = servermanager.Fetch(integ)
    cint, volume = extract_integral_and_volume(fetched)

    print("region id {}".format(rid))
    print("  bounds :", b)
    print("  volume :", volume)
    print("  paper expected volume:", expected)

    tol = max(1.0e-10, 1.0e-7 * expected)
    if not math.isclose(volume, expected, rel_tol=1.0e-7, abs_tol=tol):
        raise RuntimeError(
            "Region {} volume mismatch: got {}, expected {}. "
            "The mesh/region selection does not match Appendix 6.1."
            .format(rid, volume, expected)
        )


# ----------------------------------------------------------------------
# CSV output
# ----------------------------------------------------------------------

files = []
writers = []

try:
    for p in output_paths:
        f = open(p, "w", newline="")
        files.append(f)
        w = csv.writer(f)
        writers.append(w)

        # Keep exactly two columns for compatibility with the existing
        # bench2_dot_pandas.py.
        w.writerow(["Time", "avg(concentration)"])

    reference_volumes = [None, None, None]

    print("")
    print("Computing paper-defined averages directly in ParaView:")
    print("  avg(c3) = integral(c3 dV) / measured Volume")
    print("  pandas must NOT apply an additional factor 8 or 64")

    for k, t in enumerate(time_values):
        for i, (rid, integ, expected_volume) in enumerate(
            zip(region_ids, integrators, expected_volumes)
        ):
            integ.UpdatePipeline(time=t)
            fetched = servermanager.Fetch(integ)
            cint, measured_volume = extract_integral_and_volume(fetched)

            # Normalize exactly once, here in ParaView.
            if measured_volume <= 0.0:
                raise RuntimeError(
                    "Region {} has non-positive volume {} at t={}"
                    .format(rid, measured_volume, t)
                )
            avg = cint / measured_volume

            if reference_volumes[i] is None:
                reference_volumes[i] = measured_volume
            else:
                v0 = reference_volumes[i]
                tol = max(1.0e-11, 1.0e-8 * abs(v0))
                if abs(measured_volume - v0) > tol:
                    raise RuntimeError(
                        "Region {} volume changed with time: {} -> {} at t={}"
                        .format(rid, v0, measured_volume, t)
                    )

            writers[i].writerow([
                "{:.17g}".format(float(t)),
                "{:.17g}".format(float(avg)),
            ])

            if k == 0 or k == len(time_values) - 1:
                print(
                    "  region {:2d} | t={:.17g} | integral={:.17g} | "
                    "|Omega|={:.17g} | average={:.17g}"
                    .format(
                        rid,
                        float(t),
                        float(cint),
                        float(expected_volume),
                        float(avg),
                    )
                )

        if k == 0 or (k + 1) % 10 == 0 or k == len(time_values) - 1:
            print("Processed {}/{} time steps".format(k + 1, len(time_values)))

finally:
    for f in files:
        f.close()


print("")
for rid, p, v in zip(region_ids, output_paths, expected_volumes):
    print("region {} -> {}".format(rid, p))
    print("  normalization volume =", v)

print("")
print("Done.")
