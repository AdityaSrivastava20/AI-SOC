from pathlib import Path
import pandas as pd


# ============================================================
# STEP 1: Define project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "security_logs.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "security_features.csv"


# ============================================================
# STEP 2: Load the raw dataset
# ============================================================

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")
print("Original shape:", df.shape)


# ============================================================
# STEP 3: Display basic information
# ============================================================

print("\nOriginal columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# STEP 4: Convert timestamp to datetime
# ============================================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

print("\nTimestamp conversion completed.")


# ============================================================
# STEP 5: Check missing values
# ============================================================

print("\nMissing values before cleaning:")
print(df.isnull().sum())


# ============================================================
# STEP 6: Remove duplicate rows
# ============================================================

duplicates = df.duplicated().sum()

print("\nDuplicate rows:", duplicates)

df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)


# ============================================================
# STEP 7: Clean numeric columns
# ============================================================

df["port"] = pd.to_numeric(
    df["port"],
    errors="coerce"
)

df["bytes"] = pd.to_numeric(
    df["bytes"],
    errors="coerce"
)

df["packets"] = pd.to_numeric(
    df["packets"],
    errors="coerce"
)


# ============================================================
# STEP 8: Remove invalid numeric records
# ============================================================

df = df.dropna(
    subset=[
        "timestamp",
        "port",
        "bytes",
        "packets"
    ]
)


# ============================================================
# STEP 9: Validate port numbers
# ============================================================

df = df[
    (df["port"] >= 0) &
    (df["port"] <= 65535)
]


# ============================================================
# STEP 10: Validate bytes and packets
# ============================================================

df = df[
    (df["bytes"] >= 0) &
    (df["packets"] >= 0)
]


# ============================================================
# STEP 11: Clean protocol column
# ============================================================

df["protocol"] = (
    df["protocol"]
    .astype(str)
    .str.upper()
    .str.strip()
)


# ============================================================
# STEP 12: Clean action column
# ============================================================

df["action"] = (
    df["action"]
    .astype(str)
    .str.upper()
    .str.strip()
)


# ============================================================
# STEP 13: Create suspicious-port feature
# ============================================================

suspicious_ports = [
    21,     # FTP
    22,     # SSH
    23,     # Telnet
    25,     # SMTP
    445,    # SMB
    3389    # RDP
]

df["is_suspicious_port"] = (
    df["port"]
    .isin(suspicious_ports)
    .astype(int)
)


# ============================================================
# STEP 14: Create high-traffic feature
# ============================================================

df["is_high_traffic"] = (
    df["bytes"] > 7000
).astype(int)


# ============================================================
# STEP 15: Create high-packet feature
# ============================================================

df["is_high_packet"] = (
    df["packets"] > 50
).astype(int)


# ============================================================
# STEP 16: Create denied-action feature
# ============================================================

df["is_denied"] = (
    df["action"] == "DENY"
).astype(int)


# ============================================================
# STEP 17: Create bytes-per-packet feature
# ============================================================

df["traffic_per_packet"] = (
    df["bytes"] /
    df["packets"].replace(0, 1)
)


# ============================================================
# STEP 18: Encode protocol
# ============================================================

protocol_mapping = {
    "TCP": 1,
    "UDP": 2,
    "HTTP": 3,
    "DNS": 4
}

df["protocol_encoded"] = (
    df["protocol"]
    .map(protocol_mapping)
    .fillna(0)
    .astype(int)
)


# ============================================================
# STEP 19: Create a basic rule-based risk score
# ============================================================

df["risk_score"] = 0

# Suspicious port
df.loc[
    df["is_suspicious_port"] == 1,
    "risk_score"
] += 25

# Denied connection
df.loc[
    df["is_denied"] == 1,
    "risk_score"
] += 25

# High traffic
df.loc[
    df["is_high_traffic"] == 1,
    "risk_score"
] += 20

# High packet count
df.loc[
    df["is_high_packet"] == 1,
    "risk_score"
] += 20


# Maximum risk score = 90
df["risk_score"] = df["risk_score"].clip(
    upper=100
)


# ============================================================
# STEP 20: Create threat label
# ============================================================

def classify_threat(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


df["severity"] = df["risk_score"].apply(
    classify_threat
)


# ============================================================
# STEP 21: Check final dataset
# ============================================================

print("\nCleaned dataset shape:")
print(df.shape)

print("\nFinal columns:")
print(df.columns.tolist())

print("\nFeature preview:")
print(
    df[
        [
            "port",
            "bytes",
            "packets",
            "is_suspicious_port",
            "is_high_traffic",
            "is_high_packet",
            "is_denied",
            "traffic_per_packet",
            "protocol_encoded",
            "risk_score",
            "severity"
        ]
    ].head(10)
)


# ============================================================
# STEP 22: Check severity distribution
# ============================================================

print("\nSeverity distribution:")
print(df["severity"].value_counts())


# ============================================================
# STEP 23: Save processed dataset
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nProcessed dataset saved successfully!")

print("Output file:")
print(OUTPUT_FILE)