from pathlib import Path
import pandas as pd
import plotly.express as px

# ============================================================
# PEOPLEPULSE AI - EXPLORATORY DATA ANALYSIS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA = PROJECT_ROOT / "data" / "processed" / "employee_master.csv"

OUTPUT = PROJECT_ROOT / "images" / "eda"
OUTPUT.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("PEOPLEPULSE AI - EDA")
print("=" * 70)

df = pd.read_csv(DATA)

print(f"\nDataset Shape : {df.shape}")

# -------------------------------------------------------
# 1. Attrition Distribution
# -------------------------------------------------------

fig = px.pie(
    df,
    names="attrition",
    title="Employee Attrition Distribution"
)

fig.write_image(OUTPUT / "01_attrition_distribution.png")

print("✓ Attrition Distribution")

# -------------------------------------------------------
# 2. Department Distribution
# -------------------------------------------------------

fig = px.bar(
    df.department.value_counts().reset_index(),
    x="department",
    y="count",
    title="Employees by Department"
)

fig.write_image(OUTPUT / "02_department_distribution.png")

print("✓ Department Distribution")

# -------------------------------------------------------
# 3. Salary Distribution
# -------------------------------------------------------

fig = px.histogram(
    df,
    x="monthly_income",
    nbins=30,
    title="Monthly Income Distribution"
)

fig.write_image(OUTPUT / "03_salary_distribution.png")

print("✓ Salary Distribution")

# -------------------------------------------------------
# 4. Age Distribution
# -------------------------------------------------------

fig = px.histogram(
    df,
    x="age",
    nbins=20,
    title="Age Distribution"
)

fig.write_image(OUTPUT / "04_age_distribution.png")

print("✓ Age Distribution")

# -------------------------------------------------------
# 5. Job Satisfaction
# -------------------------------------------------------

fig = px.histogram(
    df,
    x="job_satisfaction",
    title="Job Satisfaction"
)

fig.write_image(OUTPUT / "05_job_satisfaction.png")

print("✓ Job Satisfaction")

# -------------------------------------------------------
# 6. Attrition by Department
# -------------------------------------------------------

dept = (
    df.groupby(["department","attrition"])
      .size()
      .reset_index(name="employees")
)

fig = px.bar(
    dept,
    x="department",
    y="employees",
    color="attrition",
    barmode="group",
    title="Attrition by Department"
)

fig.write_image(OUTPUT / "06_attrition_department.png")

print("✓ Attrition by Department")

# -------------------------------------------------------
# 7. Performance Rating
# -------------------------------------------------------

fig = px.histogram(
    df,
    x="performance_rating",
    title="Performance Rating Distribution"
)

fig.write_image(OUTPUT / "07_performance_rating.png")

print("✓ Performance Rating")

# -------------------------------------------------------
# 8. Income vs Attrition
# -------------------------------------------------------

fig = px.box(
    df,
    x="attrition",
    y="monthly_income",
    title="Income vs Attrition"
)

fig.write_image(OUTPUT / "08_income_attrition.png")

print("✓ Income vs Attrition")

print("\nEDA Completed Successfully!")

print(f"\nCharts saved to:\n{OUTPUT}")