# Network Intrusion Detection System (NIDS)

A machine-learning network intrusion detection system that classifies network traffic as **normal**, **DDoS**, **port scan**, or **anomaly**, then monitors a live traffic feed and raises alerts in real time.

## How it works

1. **Generate training data** — `generate_network_data.py` creates 2,000 labeled network flow records (protocol, bytes sent/received, packet count, byte rate, TCP flags, ports) with realistic patterns for normal traffic and each attack type.
2. **Train the model** — `train_nids.py` cleans the data, encodes protocol and flag fields, trains a **Random Forest** classifier, prints a classification report and confusion matrix, and saves the model to `model_nids.joblib`.
3. **Monitor live traffic** — `predict_traffic.py` polls `live_traffic.csv` every 2 seconds, classifies each new flow, and fires a color-coded alert when an attack type crosses its threshold within a 10-second window:

| Alert | Threshold (per 10 s) |
|---|---|
| DDoS | 3 flows |
| Port scan | 5 flows |
| Anomaly | 4 flows |

Alerts are also written to `realtime_log.txt` for later review.

## Project structure

```
NIDS/
├── generate_network_data.py   # Creates labeled synthetic network flows
├── network_data.csv           # Training dataset
├── train_nids.py              # Trains and evaluates the Random Forest model
├── model_nids.joblib          # Saved model
├── predict_traffic.py         # Real-time classification and alerting
├── live_traffic.csv           # Simulated live traffic feed
└── realtime_log.txt           # Alert log
```

## Run it

```bash
pip install pandas scikit-learn joblib colorama
python generate_network_data.py
python train_nids.py
python predict_traffic.py
```

## What I learned

- Which flow features separate attack traffic from normal traffic (byte rate, packet count, TCP flags, destination ports)
- How to turn model predictions into SOC-style alerts with thresholds and time windows to reduce noise
- Why alert tuning matters: too-low thresholds flood analysts, too-high thresholds miss attacks

## Next steps

- Train on a real public dataset such as CICIDS2017 or UNSW-NB15
- Feed live packet captures from Zeek or Suricata instead of a CSV
- Forward alerts into Splunk for dashboarding

*Data is synthetic and generated for lab purposes.*
