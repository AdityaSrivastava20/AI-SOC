from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "processed" / "security_features.csv"

MODEL_DIR = BASE_DIR / "ai" / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_FILE = MODEL_DIR / "threat_detection_model.pkl"


print("========================================")
print("AI-SOC ML TRAINING")
print("========================================")

print("\nProject directory:")
print(BASE_DIR)

print("\nDataset:")
print(DATA_FILE)

print("\nModel output:")
print(MODEL_FILE)


# ============================================================
# 2. CHECK DATASET
# ============================================================

if not DATA_FILE.exists():

    print("\nERROR: Dataset not found!")

    print(
        "Expected file:",
        DATA_FILE
    )

    print(
        "\nRun this first:"
    )

    print(
        "python notebooks\\feature_extraction.py"
    )

    raise SystemExit


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully!")

print("Shape:", df.shape)


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

features = [
    "port",
    "bytes",
    "packets",
    "is_suspicious_port",
    "is_high_traffic",
    "is_high_packet",
    "is_denied",
    "traffic_per_packet",
    "protocol_encoded"
]

required_columns = features + ["severity"]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Missing columns:")

    print(missing_columns)

    raise SystemExit


# ============================================================
# 5. CREATE TARGET
# ============================================================

target_mapping = {
    "LOW": 0,
    "MEDIUM": 1,
    "HIGH": 2
}

df["target"] = df["severity"].map(
    target_mapping
)


# ============================================================
# 6. REMOVE INVALID TARGETS
# ============================================================

df = df.dropna(
    subset=["target"]
)

df["target"] = df["target"].astype(int)


print("\nTarget distribution:")

print(
    df["severity"].value_counts()
)


# ============================================================
# 7. PREPARE X AND Y
# ============================================================

X = df[features]

y = df["target"]


print("\nFeatures used by ML model:")

for feature in features:

    print("-", feature)


# ============================================================
# 8. TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 9. CREATE RANDOM FOREST
# ============================================================

print("\nCreating Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# 10. TRAIN MODEL
# ============================================================

print("Training model...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")


# ============================================================
# 11. PREDICTION
# ============================================================

print("\nTesting model...")

y_pred = model.predict(
    X_test
)


# ============================================================
# 12. ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n========================================")
print("MODEL RESULT")
print("========================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# 13. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "LOW",
            "MEDIUM",
            "HIGH"
        ],
        zero_division=0
    )
)


# ============================================================
# 14. FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance:")

print(importance.to_string(index=False))


# ============================================================
# 15. SAVE MODEL
# ============================================================

print("\nSaving model...")

joblib.dump(
    {
        "model": model,
        "features": features,
        "target_mapping": target_mapping
    },
    MODEL_FILE
)


# ============================================================
# 16. VERIFY MODEL
# ============================================================

if MODEL_FILE.exists():

    print("\n========================================")
    print("SUCCESS!")
    print("========================================")

    print(
        "Model saved successfully:"
    )

    print(
        MODEL_FILE
    )

else:

    print("\nERROR: Model file was NOT created!")