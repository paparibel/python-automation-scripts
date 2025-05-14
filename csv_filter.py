import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description="Filter a CSV file by numeric column value.")
parser.add_argument("input", help="Input CSV file")
parser.add_argument("column", help="Column to filter")
parser.add_argument("threshold", type=float, help="Minimum value to include")
args = parser.parse_args()

if not os.path.exists(args.input):
    print("File not found.")
    exit(1)

df = pd.read_csv(args.input)

if args.column not in df.columns:
    print(f"Column {args.column} not found.")
    exit(1)

filtered = df[df[args.column] > args.threshold]
filtered.to_csv("filtered_output.csv", index=False)

print(f"Filtered {len(filtered)} rows. Output saved to filtered_output.csv.")
