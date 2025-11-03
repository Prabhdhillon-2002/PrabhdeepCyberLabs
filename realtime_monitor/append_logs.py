import pandas as pd
import numpy as np
import time

LOG_FILE = "log_stream.csv"

def append_logs():
    while True:
        # Generate mostly "normal" values (like system logs)
        new_data = {
            "feature1": [np.random.randint(10, 50)],   # normal range
            "feature2": [np.random.randint(20, 60)],   # normal range
            "feature3": [np.random.randint(30, 70)]    # normal range
        }

        # Occasionally inject an anomaly (outlier values)
        if np.random.rand() < 0.2:  # 20% chance
            new_data = {
                "feature1": [np.random.randint(200, 500)],  # extreme spike
                "feature2": [np.random.randint(200, 500)],
                "feature3": [np.random.randint(200, 500)]
            }
            print("[!] Injected anomaly:", new_data)

        df = pd.DataFrame(new_data)
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)

        print("[+] Appended log entry:", new_data)

        time.sleep(3)  # append every 3 seconds

if __name__ == "__main__":
    append_logs()
