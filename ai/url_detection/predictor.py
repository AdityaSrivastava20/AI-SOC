from pathlib import Path
import pickle
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "ai" / "models" / "url_model.pkl"


def predict_url(features):

    with open(MODEL_PATH, "rb") as file:
        model_data = pickle.load(file)

    model = model_data["model"]
    feature_names = model_data["features"]

    # Create DataFrame with the same feature names
    input_data = pd.DataFrame(
        [[features[name] for name in feature_names]],
        columns=feature_names
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    confidence = float(max(probabilities) * 100)

    if prediction == 1:

        if confidence >= 90:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

    else:
        severity = "LOW"

    return {
        "prediction": int(prediction),
        "severity": severity,
        "confidence": round(confidence, 2)
    }