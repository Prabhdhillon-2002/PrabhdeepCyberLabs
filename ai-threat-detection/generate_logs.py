import pandas as pd
import random

# Set random seed for reproducibility
random.seed(42)

# Generate fake system log data
def generate_logs(filename='synthetic_logs.csv', num_logs=500):
    logs = []

    for _ in range(num_logs):
        log = { 
            'cpu_usage': round(random.uniform(0, 100), 2),  # CPU usage in percentage
            'memory_usage': round(random.uniform(0, 100), 2),  # Memory usage in percentage
            'network_in': round(random.uniform(0, 1000), 2),  # Network input in MB
            'network_out': round(random.uniform(0, 1000), 2),  # Network output in MB
        }
        logs.append(log)

    # Inject anomalies
    for _ in range(10): #10 weird entries
        log = {
            'cpu_usage': round(random.uniform(150, 300), 2),  # Abnormally high CPU usage
            'memory_usage': round(random.uniform(150, 300), 2),  # Abnormally high Memory usage
            'network_in': round(random.uniform(1500, 3000), 2),  # Abnormally high Network input
            'network_out': round(random.uniform(1500, 3000), 2),  # Abnormally high Network output
        }
        logs.append(log)
        
    df = pd.DataFrame(logs)
    df.to_csv(filename, index=False)
    print(f"[SAVED] {len(df)} synthetic logs to {filename}")

if __name__ == "__main__":
    generate_logs()