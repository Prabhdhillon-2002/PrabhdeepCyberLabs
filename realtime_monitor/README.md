# Real-Time Log Anomaly Detection

This project highlights the creation of a real-time system for detecting anomalies in streaming log data using the Isolation Forest algorithm. It replicates how a Security Operations Center (SOC) would monitor system logs continuously and automatically flag unusual behavior.

# Overview

Develop a machine learning model (IsolationForest) to detect abnormal patterns in system logs.
Keep a constant watch on incoming logs to classify them as either normal or anomalous.
Mimic a real-time log feed by adding new entries to a CSV file.
Display color-coded alerts in the terminal whenever anomalies are detected.
This initiative is a component of my cybersecurity learning path, focused on blending machine learning, data analysis, and threat detection.
# Technologies
Python 3
Pandas (for handling and processing data)
Scikit-Learn (using IsolationForest for anomaly detection)
Joblib (for storing and retrieving the trained model)
Colorama (used for colored terminal alerts)
NumPy (for generating synthetic logs)
# Project structure
│── train_model.py # Trains the Isolation Forest model using log_stream.csv
│── monitor_logs.py # Monitors the log file in real time to detect anomalies
│── append_logs.py # Mimics live log entries by adding normal and anomalous data
│── log_stream.csv # Contains both the original and newly added log entries
│── model.joblib # Stores the trained Isolation Forest model

# How it works
1. Train the Model
prepare dataset ('log_stream.csv') with numeric log entries and run bash
python train_model.py - Trains an Isolation Forest model and saves it as model.joblib.
2. start the monitoring script in one terminal:
python monitor_logs.csv - It will continuosly watch for new rows in log_stream.csv and print alerts: Green = Normal logs, Red = Anomalies detected
3. in another terminal, run the appender script: python append_logs.py 
# This will add new rows every few seconds. Some rows will be normal, others will be spikes/outliers, which trigger anomaly alerts.

# Key Takeaways
Hands on experience with anomaly detection models.
real-time log monitoring.
Integration of ML into cybersecurity workflows.

# Improvements
Add more realistic log data example, network traffic, System logs. 
Integrate with SIEM dashboards like Splunk or ELK Stack
add alerting mechanisms

