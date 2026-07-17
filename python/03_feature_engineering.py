from pathlib import Path
import pandas as pd
import numpy as np

# ============================================================
# PEOPLEPULSE AI - FEATURE ENGINEERING
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEANED_DATA = PROJECT_ROOT / "data" / "cleaned"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("PEOPLEPULSE AI - FEATURE ENGINEERING")
print("=" * 70)

# ------------------------------------------------------------
# Load datasets
# ------------------------------------------------------------

general = pd.read_csv(CLEANED_DATA / "general_data.csv")
employee = pd.read_csv(CLEANED_DATA / "employee_survey_data.csv")
manager = pd.read_csv(CLEANED_DATA / "manager_survey_data.csv")

# ------------------------------------------------------------
# Merge datasets
# ------------------------------------------------------------

df = general.merge(employee, on="employee_id", how="left")

df = df.merge(manager, on="employee_id", how="left")

print(f"\nMerged Dataset Shape : {df.shape}")

# ------------------------------------------------------------
# Age Group
# ------------------------------------------------------------

df["age_group"] = pd.cut(
    df["age"],
    bins=[18, 25, 35, 45, 55, 70],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "55+"
    ]
)

# ------------------------------------------------------------
# Monthly Income Band
# ------------------------------------------------------------

df["income_band"] = pd.qcut(
    df["monthly_income"],
    q=4,
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)

# ------------------------------------------------------------
# Experience Level
# ------------------------------------------------------------

df["experience_level"] = pd.cut(
    df["total_working_years"],
    bins=[-1, 2, 5, 10, 20, 50],
    labels=[
        "Entry",
        "Junior",
        "Mid",
        "Senior",
        "Expert"
    ]
)

# ------------------------------------------------------------
# Years Since Promotion Group
# ------------------------------------------------------------

df["promotion_status"] = np.where(
    df["years_since_last_promotion"] >= 5,
    "Needs Promotion",
    "Recently Promoted"
)

# ------------------------------------------------------------
# Frequent Traveler
# ------------------------------------------------------------

df["frequent_traveler"] = np.where(
    df["business_travel"] == "Travel_Frequently",
    "Yes",
    "No"
)

# ------------------------------------------------------------
# Long Commute
# ------------------------------------------------------------

df["long_commute"] = np.where(
    df["distance_from_home"] > 15,
    "Yes",
    "No"
)

# ------------------------------------------------------------
# High Salary Hike
# ------------------------------------------------------------

df["high_salary_hike"] = np.where(
    df["percent_salary_hike"] >= 20,
    "Yes",
    "No"
)

# ------------------------------------------------------------
# Attrition Label
# ------------------------------------------------------------

df["attrition_flag"] = np.where(
    df["attrition"] == "Yes",
    1,
    0
)

# ------------------------------------------------------------
# Save processed dataset
# ------------------------------------------------------------

df.to_csv(
    PROCESSED_DATA / "employee_master.csv",
    index=False
)

print("\nFeature Engineering Completed Successfully!")

print(f"\nFinal Dataset Shape : {df.shape}")

print("\nNew Features Added:")

new_features = [
    "age_group",
    "income_band",
    "experience_level",
    "promotion_status",
    "frequent_traveler",
    "long_commute",
    "high_salary_hike",
    "attrition_flag"
]

for feature in new_features:
    print(f"✓ {feature}")

print("\nSaved to:")

print(PROCESSED_DATA / "employee_master.csv")