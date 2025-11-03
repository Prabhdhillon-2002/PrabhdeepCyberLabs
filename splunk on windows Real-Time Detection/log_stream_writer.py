import time
import random
from datetime import datetime

# === File Paths ===
APACHE_LOG = r"D:\AI_Cyber_Projects\Real-time threat detection with splunk on windows\logs\apache_access.log"
WINDOWS_LOG = r"D:\AI_Cyber_Projects\Real-time threat detection with splunk on windows\logs\windows_events.csv"


# === Fake Data ===
ip_addresses = [
    "192.168.1.5", "192.168.1.10", "192.168.1.8", "10.0.0.12", "172.16.0.4"
]
users = ["franky", "admin", "jerem7", "mahima", "ravi"]
status_codes = ["200", "401", "403"]
endpoints = ["/login", "/admin", "/about.html", "/index.html", "/orders", "/shop"]

def simulate_apache_log():
    """Append a single fake Apache log entry."""
    ip = random.choice(ip_addresses)
    user = random.choice(users)
    endpoint = random.choice(endpoints)
    status = random.choice(status_codes)
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S -0500")
    line = f'{ip} - {user} [{timestamp}] "GET {endpoint} HTTP/1.1" {status} 2326\n'

    with open(APACHE_LOG, "a") as f:
        f.write(line)
    print(f"[Apache] {line.strip()}")

def simulate_windows_event():
    """Append a single fake Windows event log entry."""
    event_codes = ["4625", "4624"]  # failed and successful logon
    event = random.choice(event_codes)
    user = random.choice(users)
    ip = random.choice(ip_addresses)
    message = "An account failed to log on." if event == "4625" else "An account was successfully logged on."
    line = f"{event},{user},{ip},{message}\n"

    with open(WINDOWS_LOG, "a") as f:
        f.write(line)
    print(f"[Windows] {line.strip()}")

# === Continuous Loop ===
print("🔥 Simulating logs in real-time. Press CTRL+C to stop.\n")

while True:
    simulate_apache_log()
    if random.random() < 0.5:  # occasionally simulate Windows events
        simulate_windows_event()
    time.sleep(random.randint(3, 7))  # wait 3–7 seconds per cycle
