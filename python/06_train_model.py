from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier
)

# ============================================================
# PEOPLEPULSE AI - MODEL TRAINING
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA = PROJECT_ROOT / "data" / "processed" / "employee_master.csv"

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("PEOPLEPULSE AI - MODEL TRAINING")
print("=" * 70)

# ============================================================
# Load Data
# ============================================================

df = pd.read_csv(DATA)

# ============================================================
# Features & Target
# ============================================================

X = df.drop(columns=[
    "employee_id",
    "attrition",
    "attrition_flag"
])

y = df["attrition_flag"]

# ============================================================
# Encode Categorical Variables
# ============================================================

encoders = {}

for col in X.select_dtypes(include="object").columns:

    encoder = LabelEncoder()

    X[col] = encoder.fit_transform(X[col].astype(str))

    encoders[col] = encoder

# ============================================================
# Train/Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

# ============================================================
# Models
# ============================================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=1000,
            random_state=42
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=42
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=300,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingClassifier(
            random_state=42
        ),

    "Extra Trees":
        ExtraTreesClassifier(
            n_estimators=300,
            random_state=42
        )
}

# ============================================================
# Train Models
# ============================================================

best_model = None
best_accuracy = 0
best_name = ""

best_predictions = None

results = []

for name, model in models.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, pred)
    precision = precision_score(y_test, pred)
    recall = recall_score(y_test, pred)
    f1 = f1_score(y_test, pred)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    results.append({

        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1

    })

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_name = name
        best_predictions = pred

# ============================================================
# Model Comparison
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Accuracy",
    ascending=False
)

results_df.to_csv(
    MODEL_DIR / "model_comparison.csv",
    index=False
)

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)
print(results_df)

# ============================================================
# Best Model
# ============================================================

print("\n" + "=" * 70)
print(f"BEST MODEL : {best_name}")
print(f"Accuracy   : {best_accuracy:.4f}")
print("=" * 70)

# ============================================================
# Save Model
# ============================================================

joblib.dump(best_model, MODEL_DIR / "attrition_model.pkl")
joblib.dump(encoders, MODEL_DIR / "label_encoders.pkl")

print("\n✓ Model Saved")
print("✓ Label Encoders Saved")

# ============================================================
# Save Classification Report
# ============================================================

report = classification_report(
    y_test,
    best_predictions,
    output_dict=True
)

report_df = pd.DataFrame(report).transpose()

report_df.to_csv(
    REPORT_DIR / "classification_report.csv"
)

print("✓ Classification Report Saved")

# ============================================================
# Feature Importance
# ============================================================

if hasattr(best_model, "feature_importances_"):

    importance = pd.DataFrame({

        "Feature": X.columns,
        "Importance": best_model.feature_importances_

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    importance.to_csv(
        MODEL_DIR / "feature_importance.csv",
        index=False
    )

    print("✓ Feature Importance Saved")

print("\nTraining Completed Successfully!")