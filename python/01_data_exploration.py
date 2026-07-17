from pathlib import Path
import pandas as pd

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw"

print("=" * 80)
print("PEOPLEPULSE AI - DATA EXPLORATION")
print("=" * 80)

csv_files = sorted(DATA_PATH.glob("*.csv"))

print(f"\nFound {len(csv_files)} CSV files\n")

for file in csv_files:
    print("=" * 80)
    print(f"FILE: {file.name}")
    print("=" * 80)

    df = pd.read_csv(file)

    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(list(df.columns))

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\n")