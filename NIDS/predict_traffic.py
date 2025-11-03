import os
import time
import random
from collections import deque, Counter
import pandas as pd
import joblib
from colorama import Fore, Style, init

# Configuration

MODE = "csv"  # "csv" for live traffic feed, or "simulate" for random packets
CSV_PATH = "live_traffic.csv"
POLL_SECONDS = 2.0
LOG_PATH = "realtime_log.txt"

ALERT_WINDOW_SECONDS = 10
ALERT_THRESHOLDS = {
    "DDOS": 3,
    "PORT_SCAN": 5,
    "ANOMALY": 4
}


# Setup

init(autoreset=True)

model_path = "model_nids.joblib"
if not os.path.exists(model_path):
    print(Fore.RED + "[ERROR] model_nids.joblib not found. Train your model first.")
    raise SystemExit(1)

model = joblib.load(model_path)
expected_features = list(model.feature_names_in_)

label_map = {0: 'NORMAL', 1: 'DDOS', 2: 'PORT_SCAN', 3: 'ANOMALY'}
color_map = {
    'NORMAL': Fore.GREEN,
    'DDOS': Fore.RED,
    'PORT_SCAN': Fore.YELLOW,
    'ANOMALY': Fore.MAGENTA,
    'UNKNOWN': Fore.WHITE
}

print(Fore.CYAN + "[INFO] Real-Time Network Intrusion Detection System Started")
print(Fore.CYAN + "Press Ctrl+C to stop.\n")



# Data Handling
def generate_random_packet():
    """Simulate network traffic data."""
    return {
        'duration': round(random.uniform(0.01, 5.0), 3),
        'protocol': random.randint(0, 2),
        'src_bytes': random.randint(10, 1500),
        'dst_bytes': random.randint(10, 8000),
        'flag': random.randint(0, 5),
        'src_port': random.randint(1024, 65535),
        'dst_port': random.choice([22, 80, 443, 8080, 53, random.randint(1024, 65535)]),
        'packet_count': random.randint(1, 2000),
        'byte_rate': round(random.uniform(100.0, 500000.0), 2),
        'pps': round(random.uniform(1.0, 20000.0), 2),
        'total_bytes': random.randint(100, 10000)
    }


def read_live_data(csv_path, last_seen_rows):
    """Read new rows appended to the CSV file."""
    if not os.path.exists(csv_path):
        return last_seen_rows, []

    df = pd.read_csv(csv_path)
    if df.empty:
        return last_seen_rows, []

    if last_seen_rows >= len(df):
        return last_seen_rows, []

    new_data = df.iloc[last_seen_rows:].copy()
    return len(df), new_data.to_dict(orient="records")


# Real-time Detection

def classify_packet(packet):
    """Classify a single packet or flow record."""
    df = pd.DataFrame([packet])
    df = df.reindex(columns=expected_features, fill_value=0)

    prediction = model.predict(df)[0]
    label = label_map.get(prediction, "UNKNOWN")

    try:
        confidence = model.predict_proba(df).max()
    except Exception:
        confidence = None

    return label, confidence


def log_event(timestamp, label):
    """Save classification results to a log file."""
    with open(LOG_PATH, "a") as log:
        log.write(f"{timestamp},{label}\n")

# Alert System

events_window = deque()

def check_alerts(timestamp, label):
    """Detect repeated attack patterns within a time window."""
    events_window.append((timestamp, label))

    # Remove old events
    cutoff = timestamp - ALERT_WINDOW_SECONDS
    while events_window and events_window[0][0] < cutoff:
        events_window.popleft()

    counts = Counter(lbl for _, lbl in events_window)
    for attack_label, threshold in ALERT_THRESHOLDS.items():
        if counts.get(attack_label, 0) >= threshold:
            print(Style.BRIGHT + color_map[attack_label] + 
                  f"[ALERT] {attack_label} detected {counts[attack_label]} times in last {ALERT_WINDOW_SECONDS}s!")


# Main Monitoring Loop

try:
    last_rows_seen = 0
    print(Fore.CYAN + f"[INFO] Mode: {MODE}")
    print(Fore.CYAN + f"[INFO] Monitoring started...\n")

    while True:
        if MODE == "simulate":
            packets = [generate_random_packet()]
        else:
            last_rows_seen, packets = read_live_data(CSV_PATH, last_rows_seen)

        if not packets:
            time.sleep(POLL_SECONDS)
            continue

        for packet in packets:
            label, confidence = classify_packet(packet)
            timestamp = time.strftime("%H:%M:%S")

            color = color_map.get(label, Fore.WHITE)
            confidence_text = f" (confidence: {confidence:.2f})" if confidence else ""

            print(color + f"[{timestamp}] Traffic classified as: {label}{confidence_text}")

            log_event(time.time(), label)
            check_alerts(time.time(), label)

        time.sleep(POLL_SECONDS)

except KeyboardInterrupt:
    print(Style.BRIGHT + Fore.CYAN + "\n[INFO] Real-time monitoring stopped by user.")
