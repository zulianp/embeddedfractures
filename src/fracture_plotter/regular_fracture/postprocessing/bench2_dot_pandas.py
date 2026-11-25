#!/usr/bin/env python3
import pandas as pd
import sys

argv = sys.argv

if len(argv) != 5:
    print(
        f"usage: {argv[0]} "
        "<input_csv1> <input_csv2> <input_csv3> <output_csv>"
    )
    sys.exit(1)

input_csv1 = argv[1]
input_csv2 = argv[2]
input_csv3 = argv[3]
output_csv = argv[4]


def read_csv(path, name):
    df = pd.read_csv(path)

    required = {"Time", "avg(concentration)"}
    missing = required.difference(df.columns)
    if missing:
        raise RuntimeError(
            f"{path}: missing columns {sorted(missing)}; "
            f"found {list(df.columns)}"
        )

    # The concentration is ALREADY normalized by the ParaView script.
    # Do not multiply by 8 or 64 here.
    df = df[["Time", "avg(concentration)"]].copy()
    df = df.rename(columns={"avg(concentration)": name})
    return df


df1 = read_csv(input_csv1, "concentration_block1")
df2 = read_csv(input_csv2, "concentration_block10")
df3 = read_csv(input_csv3, "concentration_block11")

df = (
    df1.set_index("Time")
       .join(df2.set_index("Time"), how="inner")
       .join(df3.set_index("Time"), how="inner")
)

if df.empty:
    raise RuntimeError(
        "Joined dataframe is empty: the three CSV files do not "
        "have matching Time values."
    )

# Keep the same output format as the old workflow.
df.to_csv(output_csv, header=None)

print(f"Wrote {output_csv}")
print(f"Rows: {len(df)}")
print("No additional normalization applied in pandas.")
