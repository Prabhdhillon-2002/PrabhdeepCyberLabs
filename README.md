# Prabhdeep Dhillon — Cybersecurity Labs

Hands-on security projects covering **SOC monitoring, detection engineering, network intrusion detection, and machine learning for threat detection**.

**CompTIA Security+** · B.S. Cybersecurity, DePaul University (in progress) · [LinkedIn](https://www.linkedin.com/in/prabhdeep-dhillon-ba3238205)

![Splunk threat dashboard](splunk%20on%20windows%20Real-Time%20Detection/Pictures/threats_dashboard.png)

---

## Projects

| Project | What it does | Tools |
|---|---|---|
| [**Splunk Real-Time Threat Detection**](splunk%20on%20windows%20Real-Time%20Detection) | Streams simulated Apache and Windows event logs into Splunk, detects brute-force logins, web path enumeration, and repeated failed Windows logons (Event ID 4625), and shows them on a live SOC dashboard. | Splunk Enterprise, SPL, Python |
| [**Network Intrusion Detection System (NIDS)**](NIDS) | Trains a Random Forest classifier on network flow data to label traffic as normal, DDoS, port scan, or anomaly, then watches a live traffic feed and raises color-coded alerts when thresholds are crossed. | Python, scikit-learn, pandas |
| [**Multi-Stage Phishing Incident Case Study**](SOC%20analyst%20LAB) | Tier 1 SOC write-up of a phishing campaign using a PowerShell loader, Pastebin payloads, and a Telegram C2 fallback: triage, containment, memory capture, IOC hunting, and lessons learned. *(Fictional scenario for portfolio practice.)* | SIEM, EDR, incident response |
| [**Real-Time Log Anomaly Detection**](realtime_monitor) | Continuously monitors a streaming log file and flags abnormal system behavior with an Isolation Forest model, mimicking how a SOC watches logs around the clock. | Python, scikit-learn, Colorama |
| [**AI Threat Detection**](ai-threat-detection) | Generates 500+ synthetic CPU, memory, and network logs, injects suspicious events, and detects them with unsupervised machine learning. | Python, Isolation Forest, pandas |
| [**Global Threat Map**](Global_threat_predictor) | Pulls the latest GDELT world-event data every few minutes, normalizes country codes, scores threat levels, and plots them on an interactive map. | Python, GDELT, data visualization |
| [**Deepfake Image Detector**](DEEPFAKE_IMAGE_DETECTOR) | CNN-based classifier that flags AI-generated images vs. real photos, with batch scanning and confidence scores. | Python, TensorFlow/Keras, VGG16 |
| [**Motion Detection Surveillance**](rpi_survillance) | Webcam motion detection that saves timestamped snapshots as evidence; runs on Raspberry Pi or desktop. | Python, OpenCV, Raspberry Pi |

---

## Skills demonstrated

- **SOC operations:** log ingestion, alert triage, detection rules, dashboards, incident write-ups
- **Detection engineering:** SPL searches for brute force, web path enumeration, and failed-logon patterns; Windows Event ID 4625
- **Incident response:** containment, memory capture, IOC extraction, enterprise hunting
- **Network security:** traffic classification, DDoS and port-scan detection
- **Security automation:** Python scripts for log simulation, monitoring, and alerting
- **Machine learning for security:** Random Forest, Isolation Forest, CNNs

## Other tools I work with

Wireshark · Nmap · Nessus · Suricata · Snort · CrowdStrike Falcon · Microsoft Sentinel · Metasploit · Burp Suite · Autopsy · FTK Imager · Volatility · AWS security

---

*All attack data in these labs is simulated or generated in an isolated lab environment. No real systems were targeted.*
