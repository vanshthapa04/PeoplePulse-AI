import joblib

model = joblib.load("models/attrition_model.pkl")

print("MODEL TYPE")
print(type(model))

print("\nFEATURES")

if hasattr(model, "feature_names_in_"):
    for i, feature in enumerate(model.feature_names_in_, 1):
        print(f"{i}. {feature}")
else:
    print("No feature names found.")