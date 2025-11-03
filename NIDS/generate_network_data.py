import random
import csv
import math
from datetime import datetime, timedelta

random.seed(42)

N = 2000  # number of rows to generate (change as needed)
start_time = datetime.now()

protocols = ['tcp', 'udp', 'icmp']
flags = ['SF','S0','REJ','RSTO','RSTR','SH','SYN']
labels = ['normal', 'ddos', 'port_scan', 'anomaly']

def ip():
    return "{}.{}.{}.{}".format(random.randint(1,223), random.randint(0,255), random.randint(0,255), random.randint(1,254))

def gen_normal():
    duration = round(random.expovariate(1/0.5), 3)  # mostly short sessions
    protocol = random.choices(protocols, weights=[0.7,0.25,0.05])[0]
    src_bytes = int(random.gauss(300, 150)) if protocol == 'tcp' else int(random.gauss(120,80))
    dst_bytes = int(random.gauss(400, 200))
    packet_count = max(1, int(random.gauss(20,10)))
    byte_rate = max(0.01, (src_bytes + dst_bytes) / max(1, duration))
    flag = random.choice(['SF','S0','SH'])
    src_port = random.randint(1024, 65000)
    dst_port = random.choice([80,443,22,53,8080,3389, random.randint(1024,65535)])
    return duration, protocol, src_bytes, dst_bytes, packet_count, round(byte_rate,3), flag, src_port, dst_port

def gen_ddos():
    # DDoS: many short sessions, huge dst_bytes or many packets to single target
    duration = round(random.uniform(0.01, 0.4), 3)
    protocol = random.choice(['udp','icmp','tcp'])
    src_bytes = int(random.gauss(60, 30))
    dst_bytes = int(random.gauss(2000, 1500)) + random.randint(0,5000)
    packet_count = random.randint(50, 2000)
    byte_rate = max(1.0, (src_bytes + dst_bytes) / max(0.01, duration))
    flag = random.choice(['S0','RSTO','REJ'])
    src_port = random.randint(1024, 65000)
    dst_port = random.choice([80,443,53,123, random.randint(1024,65535)])
    return duration, protocol, src_bytes, dst_bytes, packet_count, round(byte_rate,3), flag, src_port, dst_port

def gen_port_scan():
    # Many connections with tiny payloads to sequential dst ports
    duration = round(random.uniform(0.01, 0.2), 3)
    protocol = 'tcp'
    src_bytes = random.randint(0,20)
    dst_bytes = random.randint(0,10)
    packet_count = random.randint(1,5)
    byte_rate = (src_bytes + dst_bytes) / max(0.001, duration)
    flag = 'SYN'
    src_port = random.randint(1024, 65000)
    dst_port = random.randint(1, 1024)
    return duration, protocol, src_bytes, dst_bytes, packet_count, round(byte_rate,3), flag, src_port, dst_port

def gen_misc_anomaly():
    # Random weird patterns: malformed, long idle, suspicious bytes
    duration = round(random.uniform(0, 120), 3)
    protocol = random.choice(protocols)
    src_bytes = max(0, int(random.gauss(1500, 2000)))
    dst_bytes = max(0, int(random.gauss(2500, 2000)))
    packet_count = random.randint(1, 1000)
    byte_rate = (src_bytes + dst_bytes) / max(0.001, duration) if duration > 0 else (src_bytes+dst_bytes)
    flag = random.choice(flags)
    src_port = random.randint(1, 65000)
    dst_port = random.randint(1, 65535)
    return duration, protocol, src_bytes, dst_bytes, packet_count, round(byte_rate,3), flag, src_port, dst_port

rows = []
for i in range(N):
    # decide label probabilities: normal more common
    r = random.random()
    if r < 0.70:
        label = 'normal'
        vals = gen_normal()
    elif r < 0.85:
        label = 'ddos'
        vals = gen_ddos()
    elif r < 0.95:
        label = 'port_scan'
        vals = gen_port_scan()
    else:
        label = 'anomaly'
        vals = gen_misc_anomaly()

    src_ip = ip()
    dst_ip = ip()
    timestamp = (start_time + timedelta(seconds=i)).isoformat()
    duration, protocol, src_bytes, dst_bytes, packet_count, byte_rate, flag, src_port, dst_port = vals

    # Add a few engineered features
    packets_per_second = round(packet_count / max(0.001, duration), 2) if duration > 0 else packet_count
    total_bytes = src_bytes + dst_bytes

    rows.append({
        'timestamp': timestamp,
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'src_port': src_port,
        'dst_port': dst_port,
        'protocol': protocol,
        'flag': flag,
        'duration': duration,
        'src_bytes': src_bytes,
        'dst_bytes': dst_bytes,
        'total_bytes': total_bytes,
        'packet_count': packet_count,
        'byte_rate': byte_rate,
        'pps': packets_per_second,
        'label': label
    })

# Save CSV
fieldnames = ['timestamp','src_ip','dst_ip','src_port','dst_port','protocol','flag','duration','src_bytes','dst_bytes','total_bytes','packet_count','byte_rate','pps','label']
with open('network_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print("Generated network_data.csv with", N, "rows")