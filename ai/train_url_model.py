from pathlib import Path
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from url_detection.features import extract_url_features


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "urls.csv"
MODEL_PATH = BASE_DIR / "ai" / "models" / "url_model.pkl"


# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset loaded")
print("Rows:", len(df))


# Extract URL features
feature_data = []

for url in df["url"]:
    features = extract_url_features(url)
    feature_data.append(features)


X = pd.DataFrame(feature_data)
y = df["label"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))


# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train model
model.fit(X_train, y_train)


# Test model
y_pred = model.predict(X_test)


# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print()
print("Model Accuracy:", round(accuracy * 100, 2), "%")

print()
print("Classification Report:")
print(classification_report(y_test, y_pred))


# Save model
model_data = {
    "model": model,
    "features": list(X.columns)
}


MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


with open(MODEL_PATH, "wb") as file:
    pickle.dump(model_data, file)


print("URL model trained successfully")

print("Model saved at:")
print(MODEL_PATH)