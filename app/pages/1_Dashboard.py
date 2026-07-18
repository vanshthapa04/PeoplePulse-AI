import streamlit as st
from database import run_query
import plotly.express as px

st.set_page_config(layout="wide")

# =====================================
# PAGE TITLE
# =====================================

st.title("📊 PeoplePulse AI Dashboard")
st.markdown("### Employee Attrition Analytics")

# =====================================
# SIDEBAR FILTER
# =====================================

departments = run_query("""
SELECT DISTINCT department
FROM employee_master
ORDER BY department;
""")

department_list = ["All"] + departments["department"].tolist()

selected_department = st.sidebar.selectbox(
    "🏢 Department",
    department_list
)

where_clause = ""

if selected_department != "All":
    where_clause = f"WHERE department = '{selected_department}'"

# =====================================
# KPIs
# =====================================

total_employees = run_query(f"""
SELECT COUNT(*) AS total
FROM employee_master
{where_clause}
""").iloc[0]["total"]

attrition_rate = run_query(f"""
SELECT ROUND(
100.0 * SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END) / COUNT(*),
2
) AS rate
FROM employee_master
{where_clause}
""").iloc[0]["rate"]

avg_income = run_query(f"""
SELECT ROUND(AVG(monthly_income),0) AS income
FROM employee_master
{where_clause}
""").iloc[0]["income"]

avg_satisfaction = run_query(f"""
SELECT ROUND(AVG(job_satisfaction),2) AS satisfaction
FROM employee_master
{where_clause}
""").iloc[0]["satisfaction"]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("👥 Employees", f"{total_employees:,}")
kpi2.metric("📉 Attrition", f"{attrition_rate}%")
kpi3.metric("💰 Avg Income", f"₹{avg_income:,.0f}")
kpi4.metric("⭐ Job Satisfaction", avg_satisfaction)

st.divider()

# =====================================
# ATTRITION BY DEPARTMENT
# =====================================

dept = run_query(f"""
SELECT
department,
COUNT(*) FILTER (WHERE attrition='Yes') AS attrition
FROM employee_master
{where_clause}
GROUP BY department
ORDER BY attrition DESC;
""")

fig = px.bar(
    dept,
    x="department",
    y="attrition",
    title="Attrition by Department",
    color="attrition",
    color_continuous_scale="Reds"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#161B22",
    plot_bgcolor="#161B22",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =====================================
# TWO COLUMN CHARTS
# =====================================

left, right = st.columns(2)

# -------- Job Role --------

role = run_query(f"""
SELECT
job_role,
COUNT(*) FILTER (WHERE attrition='Yes') AS attrition
FROM employee_master
{where_clause}
GROUP BY job_role
ORDER BY attrition DESC;
""")

fig2 = px.bar(
    role,
    x="attrition",
    y="job_role",
    orientation="h",
    title="Attrition by Job Role",
    color="attrition",
    color_continuous_scale="Blues"
)

fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="#161B22",
    plot_bgcolor="#161B22",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=50, b=20)
)

left.plotly_chart(
    fig2,
    use_container_width=True,
    config={"displayModeBar": False}
)

# -------- Business Travel --------

travel = run_query(f"""
SELECT
business_travel,
COUNT(*) AS employees
FROM employee_master
{where_clause}
GROUP BY business_travel;
""")

fig3 = px.pie(
    travel,
    values="employees",
    names="business_travel",
    hole=0.5,
    title="Business Travel Distribution"
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="#161B22",
    plot_bgcolor="#161B22",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=50, b=20)
)

right.plotly_chart(
    fig3,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =====================================
# INCOME DISTRIBUTION
# =====================================

income = run_query(f"""
SELECT monthly_income
FROM employee_master
{where_clause}
""")

fig4 = px.histogram(
    income,
    x="monthly_income",
    nbins=30,
    title="Monthly Income Distribution"
)

fig4.update_layout(
    template="plotly_dark",
    paper_bgcolor="#161B22",
    plot_bgcolor="#161B22",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    config={"displayModeBar": False}
)