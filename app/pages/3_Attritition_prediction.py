import streamlit as st
import pandas as pd

from prediction import (
    get_employee_list,
    get_employee,
    predict_employee,
    generate_recommendations
)

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Attrition Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Attrition Prediction")
st.markdown(
    "Predict employee attrition risk using the trained Machine Learning model."
)

# ============================================
# LOAD EMPLOYEES
# ============================================

employees = get_employee_list()

employees["label"] = (
    employees["employee_id"].astype(str)
    + " • "
    + employees["job_role"]
    + " ("
    + employees["department"]
    + ")"
)

selected = st.selectbox(
    "Select Employee",
    employees["label"]
)

employee_id = int(
    selected.split(" • ")[0]
)

employee = get_employee(employee_id)

# ============================================
# EMPLOYEE DETAILS
# ============================================

st.subheader("👤 Employee Information")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Employee ID", employee["employee_id"])
    st.metric("Age", employee["age"])
    st.metric("Gender", employee["gender"])
    st.metric("Department", employee["department"])

with c2:
    st.metric("Job Role", employee["job_role"])
    st.metric("Monthly Income", f"₹{employee['monthly_income']:,}")
    st.metric("Experience", f"{employee['total_working_years']} Years")
    st.metric("Years at Company", employee["years_at_company"])

with c3:
    st.metric("Business Travel", employee["business_travel"])
    st.metric("Job Satisfaction", employee["job_satisfaction"])
    st.metric("Work Life Balance", employee["work_life_balance"])
    st.metric("Performance", employee["performance_rating"])

st.divider()

# ============================================
# PREDICT BUTTON
# ============================================

if st.button(
    "🚀 Predict Attrition",
    use_container_width=True
):

    result = predict_employee(employee)

    st.subheader("Prediction Result")

    if result["risk"] == "High":
        st.error(
            f"{result['color']} HIGH RISK"
        )

    elif result["risk"] == "Medium":
        st.warning(
            f"{result['color']} MEDIUM RISK"
        )

    else:
        st.success(
            f"{result['color']} LOW RISK"
        )

    p1, p2 = st.columns(2)

    with p1:
        st.metric(
            "Attrition Probability",
            f"{result['probability']}%"
        )

    with p2:
        st.metric(
            "Risk Level",
            result["risk"]
        )

    st.divider()

    st.subheader("💡 HR Recommendations")

    recommendations = generate_recommendations(employee)

    for recommendation in recommendations:
        st.write(f"✅ {recommendation}")

    st.divider()

    st.subheader("📊 Employee Snapshot")

    snapshot = pd.DataFrame({
        "Attribute": [
            "Department",
            "Job Role",
            "Monthly Income",
            "Years at Company",
            "Job Satisfaction",
            "Environment Satisfaction",
            "Work Life Balance",
            "Business Travel"
        ],
        "Value": [
            employee["department"],
            employee["job_role"],
            f"₹{employee['monthly_income']:,}",
            employee["years_at_company"],
            employee["job_satisfaction"],
            employee["environment_satisfaction"],
            employee["work_life_balance"],
            employee["business_travel"]
        ]
    })

    st.dataframe(
        snapshot,
        hide_index=True,
        use_container_width=True
    )