import joblib

encoders = joblib.load("models/label_encoders.pkl")

print("Available Encoders:\n")

for key, encoder in encoders.items():
    print(f"\n===== {key} =====")
    print(list(encoder.classes_))