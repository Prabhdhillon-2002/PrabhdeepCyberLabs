import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import logging
import numpy as np
import os

# ===============================
#  SETUP LOGGING
# ===============================
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# ===============================
#  LOAD DATASET
# ===============================
csv_path = "network_data.csv"

if not os.path.exists(csv_path):
	logging.error(f"File not found: {csv_path}")
	exit()

df = pd.read_csv(
	csv_path,
	dtype={
		'protocol': str,
		'flag': str
	},
	na_values=['?', 'NA', 'null', '']
)

logging.info(f"Dataset loaded successfully with {len(df)} rows and {len(df.columns)} columns.")

# ===============================
#  CLEAN AND PREPROCESS
# ===============================
# Drop irrelevant or text-based columns
drop_cols = ['timestamp', 'src_ip', 'dst_ip']
df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

# Encode categorical columns
for col in ['protocol', 'flag']:
	if col in df.columns:
		le = LabelEncoder()
		df[col] = le.fit_transform(df[col])
		logging.info(f"Encoded column: {col} -> {len(le.classes_)} unique values")

# Map labels to numeric values
label_map = {'normal': 0, 'ddos': 1, 'port_scan': 2, 'anomaly': 3}
df['label'] = df['label'].map(label_map)

# Remove rows with unmapped labels or NaNs
unmapped_rows = df['label'].isnull().sum()
if unmapped_rows > 0:
	logging.warning(f"{unmapped_rows} rows had unmapped labels. They will be dropped.")
	df = df.dropna(subset=['label'])

# ===============================
#  SPLIT FEATURES & LABELS
# ===============================
x = df.drop('label', axis=1)
y = df['label']

# Ensure all features are numeric
if not np.all(np.isfinite(x.select_dtypes(include=[np.number]))):
	logging.warning("Some feature values are non-numeric or NaN. Filling with 0.")
	x = x.fillna(0)

# Split data
x_train, x_test, y_train, y_test = train_test_split(
	x, y, test_size=0.2, random_state=42, stratify=y
)

logging.info(f"Training samples: {len(x_train)}, Testing samples: {len(x_test)}")

# ===============================
#  TRAIN RANDOM FOREST MODEL
# ===============================
model = RandomForestClassifier(
	n_estimators=200,
	random_state=42,
	class_weight='balanced',
	n_jobs=-1
)

logging.info("Training RandomForest model...")
model.fit(x_train, y_train)
logging.info("Training complete!")

# ===============================
#  EVALUATION
# ===============================
y_pred = model.predict(x_test)

logging.info("Model Evaluation:")
report = classification_report(y_test, y_pred, target_names=label_map.keys())
print("\n" + report)

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:\n", cm)

# ===============================
#  SAVE MODEL
# ===============================
model_file = "model_nids.joblib"
joblib.dump(model, model_file, compress=3)
logging.info(f"Model saved successfully as {model_file}")
print(f"\n[*] Model saved successfully as {model_file} (compressed).")

# ===============================
#  FEATURE IMPORTANCE SUMMARY
# ===============================
feature_importance = pd.DataFrame({
	'Feature': x.columns,
	'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nTop 10 Important Features:")
print(feature_importance.head(10).to_string(index=False))
