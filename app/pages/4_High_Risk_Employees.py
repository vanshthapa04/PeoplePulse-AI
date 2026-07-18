import streamlit as st

from prediction import get_all_predictions

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="High Risk Employees",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 High Risk Employees")
st.markdown(
    "Identify employees most likely to leave using the trained ML model."
)

# ============================================
# LOAD DATA
# ============================================

risk_df = get_all_predictions()

# ============================================
# SIDEBAR FILTERS
# ============================================

st.sidebar.header("Filters")

departments = sorted(
    risk_df["department"].unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Department",
    ["All"] + departments
)

min_probability = st.sidebar.slider(
    "Minimum Risk Probability (%)",
    0,
    100,
    50
)

filtered = risk_df.copy()

if selected_department != "All":
    filtered = filtered[
        filtered["department"] == selected_department
    ]

filtered = filtered[
    filtered["attrition_probability"] >= min_probability
]

# ============================================
# KPI CARDS
# ============================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Employees",
    len(risk_df)
)

c2.metric(
    "High Risk Employees",
    len(
        filtered[
            filtered["risk"] == "High"
        ]
    )
)

c3.metric(
    "Average Risk",
    f"{filtered['attrition_probability'].mean():.1f}%"
)

st.divider()

# ============================================
# TABLE
# ============================================

display_df = filtered.copy()

display_df = display_df.rename(
    columns={
        "employee_id": "Employee ID",
        "department": "Department",
        "job_role": "Job Role",
        "monthly_income": "Income",
        "years_at_company": "Years",
        "job_satisfaction": "Job Satisfaction",
        "work_life_balance": "Work Life Balance",
        "attrition_probability": "Risk %",
        "risk": "Risk"
    }
)

st.subheader("🚨 Employee Risk Ranking")

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True
)

st.download_button(
    "⬇ Download Risk Report",
    display_df.to_csv(index=False).encode(),
    "high_risk_employees.csv",
    "text/csv",
    use_container_width=True
)

st.success(
    f"Showing {len(display_df)} employees."
)