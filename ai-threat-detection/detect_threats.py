import pandas as pd
from sklearn.ensemble import IsolationForest

# Load synthetic logs
df = pd.read_csv('synthetic_logs.csv')

# Create the Isolation Forest model
model = IsolationForest(
    n_estimators=100,                                       # Number of decision trees
    contamination=0.02,                                     # Estimated proportion of anomalies
    random_state=42                                         # For reproducibility
)

# Train the model
model.fit(df)

# Predict anomalies
df['anomaly'] = model.predict(df)

# Show only the detected anomalies
anomalies = df[df['anomaly'] == -1]
print("[!] Detected Anomalies: \n")
print(anomalies)

# Save anamolies to a CSV file
anomalies.to_csv('detected_anomalies.csv', index=False)
print(f"\n[SAVED] Anomalies to detected_anomalies.csv")