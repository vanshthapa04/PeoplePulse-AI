import streamlit as st
import pandas as pd
from database import run_query

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Employee Explorer",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Employee Explorer")
st.markdown("Search, filter and explore employee records.")

# ============================================
# LOAD FILTER VALUES
# ============================================

departments = run_query("""
SELECT DISTINCT department
FROM employee_master
ORDER BY department;
""")

genders = run_query("""
SELECT DISTINCT gender
FROM employee_master
ORDER BY gender;
""")

job_roles = run_query("""
SELECT DISTINCT job_role
FROM employee_master
ORDER BY job_role;
""")

# ============================================
# SIDEBAR
# ============================================

st.sidebar.header("🔎 Filters")

selected_department = st.sidebar.selectbox(
    "Department",
    ["All"] + departments["department"].tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + genders["gender"].tolist()
)

selected_job = st.sidebar.selectbox(
    "Job Role",
    ["All"] + job_roles["job_role"].tolist()
)

selected_attrition = st.sidebar.selectbox(
    "Attrition",
    ["All", "Yes", "No"]
)

search_id = st.sidebar.text_input(
    "Employee ID"
)

# ============================================
# BUILD WHERE CLAUSE
# ============================================

conditions = []

if selected_department != "All":
    conditions.append(
        f"department = '{selected_department}'"
    )

if selected_gender != "All":
    conditions.append(
        f"gender = '{selected_gender}'"
    )

if selected_job != "All":
    conditions.append(
        f"job_role = '{selected_job}'"
    )

if selected_attrition != "All":
    conditions.append(
        f"attrition = '{selected_attrition}'"
    )

if search_id.strip():

    if search_id.isdigit():

        conditions.append(
            f"employee_id = {search_id}"
        )

where_clause = ""

if conditions:
    where_clause = "WHERE " + " AND ".join(conditions)

# ============================================
# KPIs
# ============================================

kpis = run_query(f"""
SELECT

COUNT(*) AS employees,

ROUND(AVG(monthly_income),0) AS avg_income,

ROUND(AVG(total_working_years),1) AS avg_experience,

ROUND(
100.0 *
SUM(
CASE
WHEN attrition='Yes'
THEN 1
ELSE 0
END
)
/COUNT(*),
2
) AS attrition_rate

FROM employee_master

{where_clause}

""")

employees = int(kpis.iloc[0]["employees"])

avg_income = float(kpis.iloc[0]["avg_income"])

avg_experience = float(kpis.iloc[0]["avg_experience"])

attrition_rate = float(kpis.iloc[0]["attrition_rate"])

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👥 Employees",
    f"{employees:,}"
)

c2.metric(
    "💰 Avg Income",
    f"₹{avg_income:,.0f}"
)

c3.metric(
    "📈 Avg Experience",
    avg_experience
)

c4.metric(
    "📉 Attrition",
    f"{attrition_rate}%"
)

st.divider()
# ============================================
# EMPLOYEE TABLE
# ============================================

employees_df = run_query(f"""
SELECT

employee_id,
age,
gender,
department,
job_role,
monthly_income,
total_working_years,
job_satisfaction,
performance_rating,
business_travel,
work_life_balance,
attrition

FROM employee_master

{where_clause}

ORDER BY employee_id;

""")

st.subheader("📋 Employee Records")

st.dataframe(
    employees_df,
    use_container_width=True,
    hide_index=True
)

# ============================================
# DOWNLOAD CSV
# ============================================

csv = employees_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="employee_data.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# ============================================
# EMPLOYEE SUMMARY
# ============================================

st.subheader("📈 Employee Summary")

left, right = st.columns(2)

with left:

    dept_summary = run_query(f"""
    SELECT

    department,
    COUNT(*) AS employees

    FROM employee_master

    {where_clause}

    GROUP BY department

    ORDER BY employees DESC;

    """)

    st.bar_chart(
        dept_summary.set_index("department")
    )

with right:

    gender_summary = run_query(f"""
    SELECT

    gender,
    COUNT(*) AS employees

    FROM employee_master

    {where_clause}

    GROUP BY gender;

    """)

    st.bar_chart(
        gender_summary.set_index("gender")
    )

# ============================================
# ATTRITION BREAKDOWN
# ============================================

st.subheader("📉 Attrition Overview")

attrition_df = run_query(f"""
SELECT

attrition,
COUNT(*) AS employees

FROM employee_master

{where_clause}

GROUP BY attrition;

""")

st.bar_chart(
    attrition_df.set_index("attrition")
)

st.success(
    f"Showing {len(employees_df)} employee records."
)