# AI Threat Detection (Fake Logs + Isolation Forest)
This project simulates SOC workflow by generating synthetic system logs and detecting anamolies using machine learning. 
It's begginer friendly but powerful cybersecurity tool. 

# Overview
This project demonstrates how to: 
 - Generate synthetic logs that looks like CPU, memory, and network activity. 
 - Inject anomalous events (e.g., CPU Spikes, abnormal network usage)
 - Apply Isolation Forest (unsupervised Machine Learning model) to detect suspicious behavior.
 - Export results to CSV for further analysi.

 # Features 
 - Creates 500+ fake logs.
 - adds suspicious activity 
 - uses Scrikit-learn's Isolation Forest 
 - generates 'synthetic_logs.csv' and 'anomalies_detected.csv'
 - runs inside a Python virtual environment.

 # Stacks
  - Python 
  - Libraries: Pandas, Scikit-learn
  - Tools: VS Code, Virtual Environments (venv)
