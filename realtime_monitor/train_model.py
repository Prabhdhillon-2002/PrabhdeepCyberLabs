import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# load data
df = pd.read_csv("log_stream.csv")

# Train model
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(df)

# Save model
joblib.dump(model, "model.joblib")
print("Model trained and saved as model.joblib")