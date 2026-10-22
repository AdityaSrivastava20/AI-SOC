from ai.url_detection.features import extract_url_features
from ai.url_detection.predictor import predict_url


def calculate_risk_score(prediction, features):

    severity = prediction["severity"]

    if severity == "HIGH":
        return 90

    if severity == "MEDIUM":
        return 60

    # LOW
    return 10


def scan_url(url: str):

    # Step 1: Extract URL features
    features = extract_url_features(url)

    # Step 2: ML prediction
    prediction = predict_url(features)

    # Step 3: Calculate risk score
    risk_score = calculate_risk_score(
        prediction,
        features
    )

    # Step 4: Return scan result
    return {
        "url": url,
        "prediction": prediction["prediction"],
        "severity": prediction["severity"],
        "confidence": prediction["confidence"],
        "risk_score": risk_score,
        "features": features
    }