from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay
)

# ============================================================
# PEOPLEPULSE AI - MODEL EVALUATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA = PROJECT_ROOT / "data" / "processed" / "employee_master.csv"

MODEL_PATH = PROJECT_ROOT / "models" / "attrition_model.pkl"
COMPARISON_PATH = PROJECT_ROOT / "models" / "model_comparison.csv"

IMAGE_DIR = PROJECT_ROOT / "images" / "ml"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("PEOPLEPULSE AI - MODEL EVALUATION")
print("=" * 70)

# ============================================================
# Load Data
# ============================================================

df = pd.read_csv(DATA)

X = df.drop(columns=[
    "employee_id",
    "attrition",
    "attrition_flag"
])

y = df["attrition_flag"]

# ============================================================
# Encode Categorical Features
# ============================================================

for col in X.select_dtypes(include="object").columns:

    encoder = LabelEncoder()

    X[col] = encoder.fit_transform(X[col].astype(str))

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

# ============================================================
# Load Model
# ============================================================

model = joblib.load(MODEL_PATH)

pred = model.predict(X_test)

prob = model.predict_proba(X_test)[:, 1]

# ============================================================
# Metrics
# ============================================================

accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred)
recall = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)
auc = roc_auc_score(y_test, prob)

metrics = pd.DataFrame({

    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ],

    "Value": [
        accuracy,
        precision,
        recall,
        f1,
        auc
    ]

})

metrics.to_csv(
    REPORT_DIR / "model_metrics.csv",
    index=False
)

print(metrics)

# ============================================================
# Confusion Matrix
# ============================================================

disp = ConfusionMatrixDisplay.from_predictions(
    y_test,
    pred
)

plt.title("Confusion Matrix")
plt.tight_layout()

plt.savefig(
    IMAGE_DIR / "confusion_matrix.png",
    dpi=300
)

plt.close()

print("✓ Confusion Matrix Saved")

# ============================================================
# ROC Curve
# ============================================================

RocCurveDisplay.from_predictions(
    y_test,
    prob
)

plt.title("ROC Curve")
plt.tight_layout()

plt.savefig(
    IMAGE_DIR / "roc_curve.png",
    dpi=300
)

plt.close()

print("✓ ROC Curve Saved")

# ============================================================
# Precision Recall Curve
# ============================================================

PrecisionRecallDisplay.from_predictions(
    y_test,
    prob
)

plt.title("Precision Recall Curve")
plt.tight_layout()

plt.savefig(
    IMAGE_DIR / "precision_recall_curve.png",
    dpi=300
)

plt.close()

print("✓ Precision Recall Curve Saved")

# ============================================================
# Feature Importance
# ============================================================

if hasattr(model, "feature_importances_"):

    importance = pd.DataFrame({

        "Feature": X.columns,
        "Importance": model.feature_importances_

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    ).head(15)

    plt.figure(figsize=(10, 6))

    plt.barh(
        importance["Feature"],
        importance["Importance"]
    )

    plt.xlabel("Importance")
    plt.title("Top 15 Important Features")

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.savefig(
        IMAGE_DIR / "feature_importance.png",
        dpi=300
    )

    plt.close()

    print("✓ Feature Importance Chart Saved")

# ============================================================
# Model Comparison
# ============================================================

comparison = pd.read_csv(COMPARISON_PATH)

plt.figure(figsize=(10, 5))

plt.bar(
    comparison["Model"],
    comparison["Accuracy"]
)

plt.ylabel("Accuracy")
plt.title("Model Comparison")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    IMAGE_DIR / "model_comparison.png",
    dpi=300
)

plt.close()

print("✓ Model Comparison Saved")

print("\nEvaluation Completed Successfully!")