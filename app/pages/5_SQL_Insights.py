import streamlit as st
import plotly.express as px
from database import run_query

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="SQL Insights",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ SQL Insights")
st.markdown("Business insights generated directly from PostgreSQL queries.")

# ============================================
# QUERY 1
# ============================================

dept_attrition = run_query("""
SELECT
    department,
    COUNT(*) AS employees,
    SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END) AS attritions,
    ROUND(
        100.0 *
        SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS attrition_rate
FROM employee_master
GROUP BY department
ORDER BY attrition_rate DESC;
""")

# ============================================
# QUERY 2
# ============================================

income = run_query("""
SELECT
    department,
    ROUND(AVG(monthly_income),0) AS avg_income
FROM employee_master
GROUP BY department
ORDER BY avg_income DESC;
""")

# ============================================
# QUERY 3
# ============================================

satisfaction = run_query("""
SELECT
    job_satisfaction,
    COUNT(*) AS employees
FROM employee_master
GROUP BY job_satisfaction
ORDER BY job_satisfaction;
""")

# ============================================
# QUERY 4
# ============================================

travel = run_query("""
SELECT
    business_travel,
    COUNT(*) AS employees
FROM employee_master
GROUP BY business_travel
ORDER BY employees DESC;
""")

# ============================================
# CHARTS
# ============================================

c1, c2 = st.columns(2)

with c1:

    st.subheader("Attrition by Department")

    fig = px.bar(
        dept_attrition,
        x="department",
        y="attrition_rate",
        text="attrition_rate",
        template="plotly_dark"
    )

    fig.update_layout(height=420)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with c2:

    st.subheader("Average Income")

    fig = px.bar(
        income,
        x="department",
        y="avg_income",
        text="avg_income",
        template="plotly_dark"
    )

    fig.update_layout(height=420)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ============================================

c3, c4 = st.columns(2)

with c3:

    st.subheader("Job Satisfaction")

    fig = px.pie(
        satisfaction,
        values="employees",
        names="job_satisfaction",
        hole=.45,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with c4:

    st.subheader("Business Travel")

    fig = px.bar(
        travel,
        x="business_travel",
        y="employees",
        text="employees",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

st.divider()

# ============================================
# SQL TABLES
# ============================================

st.subheader("Department Attrition")

st.dataframe(
    dept_attrition,
    hide_index=True,
    use_container_width=True
)

st.subheader("Average Income by Department")

st.dataframe(
    income,
    hide_index=True,
    use_container_width=True
)