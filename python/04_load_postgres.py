from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ============================================================
# PEOPLEPULSE AI - LOAD DATA TO POSTGRESQL
# ============================================================

print("=" * 70)
print("PEOPLEPULSE AI - LOAD DATA TO POSTGRESQL")
print("=" * 70)

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEANED_DATA = PROJECT_ROOT / "data" / "cleaned"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

# ------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ------------------------------------------------------------

load_dotenv(PROJECT_ROOT / ".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# ------------------------------------------------------------
# LOAD CSV FILES
# ------------------------------------------------------------

employees = pd.read_csv(CLEANED_DATA / "general_data.csv")
employee_surveys = pd.read_csv(CLEANED_DATA / "employee_survey_data.csv")
manager_surveys = pd.read_csv(CLEANED_DATA / "manager_survey_data.csv")
employee_master = pd.read_csv(PROCESSED_DATA / "employee_master.csv")

print("\nDatasets Loaded Successfully")
print(f"Employees           : {employees.shape}")
print(f"Employee Surveys    : {employee_surveys.shape}")
print(f"Manager Surveys     : {manager_surveys.shape}")
print(f"Employee Master     : {employee_master.shape}")

# ------------------------------------------------------------
# DELETE OLD DATA
# ------------------------------------------------------------

print("\nDeleting existing records...")

try:
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM employee_master;"))
        conn.execute(text("DELETE FROM manager_surveys;"))
        conn.execute(text("DELETE FROM employee_surveys;"))
        conn.execute(text("DELETE FROM employees;"))

    print("✓ Existing data deleted successfully")

except Exception as e:
    print(f"\nError while deleting existing data:\n{e}")
    raise

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\nLoading data into PostgreSQL...")

try:

    employees.to_sql(
        "employees",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("✓ Employees Loaded")

    employee_surveys.to_sql(
        "employee_surveys",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("✓ Employee Surveys Loaded")

    manager_surveys.to_sql(
        "manager_surveys",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("✓ Manager Surveys Loaded")

    employee_master.to_sql(
        "employee_master",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("✓ Employee Master Loaded")

except Exception as e:
    print(f"\nError while loading data:\n{e}")
    raise

# ------------------------------------------------------------
# VERIFY COUNTS
# ------------------------------------------------------------

print("\nVerifying data...")

tables = [
    "employees",
    "employee_surveys",
    "manager_surveys",
    "employee_master"
]

with engine.connect() as conn:
    for table in tables:
        count = conn.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar()

        print(f"{table:<20}: {count}")

print("\n" + "=" * 70)
print("DATA LOADED SUCCESSFULLY")
print("=" * 70)