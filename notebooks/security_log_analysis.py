import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# STEP 1: Load the dataset
# ==========================================

file_path = "../data/raw/security_logs.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")


# ==========================================
# STEP 2: Display first 5 rows
# ==========================================

print("\nFirst 5 rows:")
print(df.head())


# ==========================================
# STEP 3: Display last 5 rows
# ==========================================

print("\nLast 5 rows:")
print(df.tail())


# ==========================================
# STEP 4: Check number of rows and columns
# ==========================================

print("\nDataset shape:")
print(df.shape)

print("\nNumber of rows:", df.shape[0])
print("Number of columns:", df.shape[1])


# ==========================================
# STEP 5: Display column names
# ==========================================

print("\nColumn names:")
print(df.columns)


# ==========================================
# STEP 6: Check data types
# ==========================================

print("\nData types:")
print(df.dtypes)


# ==========================================
# STEP 7: Check missing values
# ==========================================

print("\nMissing values:")
print(df.isnull().sum())


# ==========================================
# STEP 8: Check duplicate records
# ==========================================

print("\nNumber of duplicate rows:")
print(df.duplicated().sum())


# ==========================================
# STEP 9: Basic statistical analysis
# ==========================================

print("\nStatistical summary:")
print(df.describe())


# ==========================================
# STEP 10: Analyze network protocols
# ==========================================

print("\nProtocol distribution:")
print(df["protocol"].value_counts())


# ==========================================
# STEP 11: Analyze actions
# ==========================================

print("\nAction distribution:")
print(df["action"].value_counts())


# ==========================================
# STEP 12: Analyze destination ports
# ==========================================

print("\nDestination port distribution:")
print(df["port"].value_counts())


# ==========================================
# STEP 13: Analyze source IP addresses
# ==========================================

print("\nSource IP distribution:")
print(df["source_ip"].value_counts())


# ==========================================
# STEP 14: Analyze traffic by bytes
# ==========================================

print("\nTop 10 records by bytes:")
print(
    df.sort_values(
        by="bytes",
        ascending=False
    ).head(10)
)


# ==========================================
# STEP 15: Analyze traffic by packets
# ==========================================

print("\nTop 10 records by packets:")
print(
    df.sort_values(
        by="packets",
        ascending=False
    ).head(10)
)


# ==========================================
# STEP 16: Find denied connections
# ==========================================

denied_logs = df[df["action"] == "DENY"]

print("\nDenied connections:")
print(denied_logs)

print("\nNumber of denied connections:", len(denied_logs))


# ==========================================
# STEP 17: Find allowed connections
# ==========================================

allowed_logs = df[df["action"] == "ALLOW"]

print("\nNumber of allowed connections:", len(allowed_logs))


# ==========================================
# STEP 18: Analyze suspicious ports
# ==========================================

suspicious_ports = [21, 22, 23, 445, 3389]

suspicious_logs = df[
    df["port"].isin(suspicious_ports)
]

print("\nLogs using suspicious ports:")
print(suspicious_logs)

print(
    "\nNumber of logs using suspicious ports:",
    len(suspicious_logs)
)


# ==========================================
# STEP 19: Analyze high packet traffic
# ==========================================

high_packet_logs = df[
    df["packets"] > 50
]

print("\nHigh packet traffic:")
print(high_packet_logs)


# ==========================================
# STEP 20: Analyze high byte traffic
# ==========================================

high_byte_logs = df[
    df["bytes"] > 7000
]

print("\nHigh byte traffic:")
print(high_byte_logs)


# ==========================================
# STEP 21: Protocol + Action analysis
# ==========================================

print("\nProtocol and action analysis:")

protocol_action = pd.crosstab(
    df["protocol"],
    df["action"]
)

print(protocol_action)


# ==========================================
# STEP 22: Port + Action analysis
# ==========================================

print("\nPort and action analysis:")

port_action = pd.crosstab(
    df["port"],
    df["action"]
)

print(port_action)


# ==========================================
# STEP 23: Create visualizations
# ==========================================

# Action distribution
plt.figure(figsize=(6, 4))

sns.countplot(
    data=df,
    x="action"
)

plt.title("Allowed vs Denied Connections")
plt.xlabel("Action")
plt.ylabel("Number of Connections")

plt.show()


# Protocol distribution
plt.figure(figsize=(6, 4))

sns.countplot(
    data=df,
    x="protocol"
)

plt.title("Network Protocol Distribution")
plt.xlabel("Protocol")
plt.ylabel("Number of Connections")

plt.show()


# Port distribution
plt.figure(figsize=(10, 5))

sns.countplot(
    data=df,
    x="port"
)

plt.title("Destination Port Distribution")
plt.xlabel("Port")
plt.ylabel("Number of Connections")

plt.xticks(rotation=45)

plt.show()


# Bytes distribution
plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="bytes",
    bins=10,
    kde=True
)

plt.title("Network Traffic by Bytes")
plt.xlabel("Bytes")
plt.ylabel("Frequency")

plt.show()


# Packets distribution
plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="packets",
    bins=10,
    kde=True
)

plt.title("Network Traffic by Packets")
plt.xlabel("Packets")
plt.ylabel("Frequency")

plt.show()