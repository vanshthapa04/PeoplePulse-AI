import joblib
import pandas as pd
from database import run_query

# ============================================
# LOAD MODEL & ENCODERS
# ============================================

model = joblib.load("models/attrition_model.pkl")
encoders = joblib.load("models/label_encoders.pkl")

# ============================================
# MODEL FEATURES
# ============================================

MODEL_FEATURES = list(model.feature_names_in_)

CATEGORICAL_COLUMNS = [
    "business_travel",
    "department",
    "education_field",
    "gender",
    "job_role",
    "marital_status",
    "age_group",
    "income_band",
    "experience_level",
    "promotion_status",
    "frequent_traveler",
    "long_commute",
    "high_salary_hike",
]

# ============================================
# FETCH EMPLOYEE IDS
# ============================================

def get_employee_list():
    return run_query("""
        SELECT
            employee_id,
            job_role,
            department
        FROM employee_master
        ORDER BY employee_id;
    """)

# ============================================
# FETCH EMPLOYEE DETAILS
# ============================================

def get_employee(employee_id):

    query = f"""
        SELECT *
        FROM employee_master
        WHERE employee_id = {employee_id};
    """

    df = run_query(query)

    if df.empty:
        return None

    return df.iloc[0]

# ============================================
# PREPARE MODEL INPUT
# ============================================

def prepare_features(employee):

    data = employee.copy()

    for column in CATEGORICAL_COLUMNS:

        if column in data.index:

            encoder = encoders[column]

            value = data[column]

            try:
                data[column] = encoder.transform([value])[0]

            except Exception:
                data[column] = 0

    input_df = pd.DataFrame([data])

    input_df = input_df[MODEL_FEATURES]

    return input_df

# ============================================
# PREDICT
# ============================================

def predict_employee(employee):

    X = prepare_features(employee)

    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0][1]

    if probability < 0.30:
        risk = "Low"
        color = "🟢"

    elif probability < 0.70:
        risk = "Medium"
        color = "🟠"

    else:
        risk = "High"
        color = "🔴"

    return {
        "prediction": prediction,
        "probability": round(probability * 100, 2),
        "risk": risk,
        "color": color
    }

# ============================================
# GENERATE RECOMMENDATIONS
# ============================================

def generate_recommendations(employee):

    recommendations = []

    if employee["job_satisfaction"] <= 2:
        recommendations.append(
            "Improve employee engagement and job satisfaction."
        )

    if employee["work_life_balance"] <= 2:
        recommendations.append(
            "Review workload and improve work-life balance."
        )

    if employee["environment_satisfaction"] <= 2:
        recommendations.append(
            "Assess workplace environment and culture."
        )

    if employee["frequent_traveler"] == "Yes":
        recommendations.append(
            "Reduce unnecessary business travel where possible."
        )

    if employee["long_commute"] == "Yes":
        recommendations.append(
            "Consider flexible or hybrid work arrangements."
        )

    if employee["promotion_status"] == "Needs Promotion":
        recommendations.append(
            "Review promotion and career growth opportunities."
        )

    if employee["monthly_income"] < 5000:
        recommendations.append(
            "Review compensation and employee benefits."
        )

    if not recommendations:
        recommendations.append(
            "No major HR concerns detected. Continue regular engagement."
        )

    return recommendations
# ============================================
# SCORE ALL EMPLOYEES
# ============================================

def get_all_predictions():

    df = run_query("""
        SELECT *
        FROM employee_master
        ORDER BY employee_id;
    """)

    results = []

    for _, employee in df.iterrows():

        prediction = predict_employee(employee)

        results.append({
            "employee_id": employee["employee_id"],
            "department": employee["department"],
            "job_role": employee["job_role"],
            "monthly_income": employee["monthly_income"],
            "years_at_company": employee["years_at_company"],
            "job_satisfaction": employee["job_satisfaction"],
            "work_life_balance": employee["work_life_balance"],
            "attrition_probability": prediction["probability"],
            "risk": prediction["risk"]
        })

    results_df = pd.DataFrame(results)

    return results_df.sort_values(
        "attrition_probability",
        ascending=False
    )