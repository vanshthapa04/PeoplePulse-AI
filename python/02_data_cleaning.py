from pathlib import Path
import pandas as pd

# ============================================================
# PEOPLEPULSE AI - DATA CLEANING
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw"
CLEANED_DATA = PROJECT_ROOT / "data" / "cleaned"

CLEANED_DATA.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def snake_case(df):
    """Convert column names to snake_case."""
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace(r"([a-z])([A-Z])", r"\1_\2", regex=True)
        .str.lower()
    )
    return df


def fill_numeric_median(df, columns):
    """Fill missing numeric values using median."""
    for col in columns:
        if col in df.columns:
            missing = df[col].isnull().sum()
            if missing > 0:
                median = df[col].median()
                df[col] = df[col].fillna(median)
                print(f"✓ Filled {missing} missing values in '{col}' using median ({median})")


def drop_constant_columns(df):
    """Drop columns containing only one unique value."""
    constant_cols = []

    for col in df.columns:
        if df[col].nunique(dropna=False) == 1:
            constant_cols.append(col)

    if constant_cols:
        df.drop(columns=constant_cols, inplace=True)
        print(f"✓ Removed constant columns: {constant_cols}")

    return df


# ============================================================
# GENERAL DATA
# ============================================================

print("=" * 70)
print("GENERAL DATA")
print("=" * 70)

general = pd.read_csv(RAW_DATA / "general_data.csv")

general = snake_case(general)

print(f"Original Shape : {general.shape}")

general = drop_constant_columns(general)

fill_numeric_median(
    general,
    [
        "num_companies_worked",
        "total_working_years"
    ]
)

print(f"Final Shape    : {general.shape}")

general.to_csv(
    CLEANED_DATA / "general_data.csv",
    index=False
)

print("✓ Saved cleaned general_data.csv\n")


# ============================================================
# EMPLOYEE SURVEY
# ============================================================

print("=" * 70)
print("EMPLOYEE SURVEY")
print("=" * 70)

employee = pd.read_csv(RAW_DATA / "employee_survey_data.csv")

employee = snake_case(employee)

print(f"Original Shape : {employee.shape}")

fill_numeric_median(
    employee,
    [
        "environment_satisfaction",
        "job_satisfaction",
        "work_life_balance"
    ]
)

print(f"Final Shape    : {employee.shape}")

employee.to_csv(
    CLEANED_DATA / "employee_survey_data.csv",
    index=False
)

print("✓ Saved cleaned employee_survey_data.csv\n")


# ============================================================
# MANAGER SURVEY
# ============================================================

print("=" * 70)
print("MANAGER SURVEY")
print("=" * 70)

manager = pd.read_csv(RAW_DATA / "manager_survey_data.csv")

manager = snake_case(manager)

print(f"Original Shape : {manager.shape}")

print("✓ No missing values found")

manager.to_csv(
    CLEANED_DATA / "manager_survey_data.csv",
    index=False
)

print("✓ Saved cleaned manager_survey_data.csv\n")


# ============================================================
# SUMMARY
# ============================================================

print("=" * 70)
print("DATA CLEANING COMPLETED")
print("=" * 70)

print(f"General Data      : {general.shape}")
print(f"Employee Survey   : {employee.shape}")
print(f"Manager Survey    : {manager.shape}")

print("\n✓ Cleaned datasets saved to:")
print(CLEANED_DATA)