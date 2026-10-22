from pathlib import Path
import joblib
import pandas as pd


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model path
MODEL_FILE = BASE_DIR / "ai" / "models" / "threat_detection_model.pkl"


# Check model exists
if not MODEL_FILE.exists():
    print("❌ Model file not found!")
    print(f"Expected location: {MODEL_FILE}")
    exit()


# Load model
saved_model = joblib.load(MODEL_FILE)

model = saved_model["model"]
features = saved_model["features"]


# Example security log
log_data = {
    "port": 3389,
    "bytes": 8100,
    "packets": 70,
    "is_suspicious_port": 1,
    "is_high_traffic": 1,
    "is_high_packet": 1,
    "is_denied": 1,
    "traffic_per_packet": 8100 / 70,
    "protocol_encoded": 1
}


# Convert to DataFrame
input_data = pd.DataFrame([log_data])

# Make sure feature order is correct
input_data = input_data[features]


# Prediction
prediction = model.predict(input_data)[0]

# Prediction probability
probability = model.predict_proba(input_data)[0]

confidence = max(probability) * 100


# Convert prediction number to severity
severity_mapping = {
    0: "LOW",
    1: "MEDIUM",
    2: "HIGH"
}

severity = severity_mapping[prediction]


print("\n==============================")
print("     AI-SOC THREAT DETECTION")
print("==============================")

print(f"Port       : {log_data['port']}")
print(f"Bytes      : {log_data['bytes']}")
print(f"Packets    : {log_data['packets']}")
print(f"Prediction : {severity}")
print(f"Confidence : {confidence:.2f}%")

print("==============================")