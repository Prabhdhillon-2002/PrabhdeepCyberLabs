# Overview

This project demonstrates how to build a **real-time cybersecurity threat detection dashboard** using **Splunk Enterprise**.  
It simulates real-world network and Windows event logs, detects suspicious activities such as **brute-force attacks, web path enumeration, and failed logins**, and visualizes them like a real **Security Operations Center (SOC)** dashboard.

# How It Works

1. **Log Simulation:**  
   A Python script continuously writes new log entries to both Apache access logs and Windows event logs.

2. **Data Ingestion:**  
   Splunk monitors these log files and automatically indexes new events in real-time.

3. **Detection Queries (SPL):**  
   Three detection rules analyze patterns of suspicious activity:
   - Brute Force Logins  
   - Web Path Enumeration (one IP probing many different URLs)  
   - Excessive Windows Logon Failures

4. **Visualization:**  
   The results are displayed in a single Splunk dashboard called **“Threat Dashboard”**, which updates live.

# Folder Structure 

Real-time-threat-detection/
│
├── logs/
│ ├── apache_access.log
│ └── windows_events.csv
│
├── detection_queries/
│ ├── brute_force_search.spl
│ ├── web_path_enumeration.spl
│ └── windows_failed_logins.spl
│
├── log_stream_writer.py
├── threats_dashboard.png
└── README.md

# Setup Instructions
1. **Install Splunk Enterprise**
   - Download from: https://www.splunk.com/en_us/download/splunk-enterprise.html  
   - Run the installer and open: `http://localhost:8000`  
   - Log in with your admin credentials.

2. **Add Data Inputs**
   - Go to **Settings → Add Data → Upload**
   - Upload both files:
     - `apache_access.log` → sourcetype = `access_combined`
     - `windows_events.csv` → sourcetype = `csv`
   - Set index name to **security** for both.
   - Verify data using:
     spl
     index=security

3. **Run Log Simulation**
   - Open Command Prompt or PowerShell:
     cd "Z:Cyber_Projects\Real-time threat detection with Splunk on Windows"
     python log_stream_writer.py
   - This script keeps generating new log data so Splunk updates in real-time.

# Create a Dashboard

Go to Search & Reporting → Dashboards → Create New Dashboard
Title: Threat Dashboard
Add three panels using the saved reports:
- Brute Force Detection (Table)
- Web Path Enumeration (Bar Chart)
- Excessive Windows Failed Logins (Table)
Set dashboard auto-refresh to 30 seconds.

 final dashboard showcasing all detections in **Threats_dashboard.png**

 # Tools

 - Splunk enterprise 
 - Python
 - Apache Access Logs
 - Windows Event Logs (CSV)

 # Takeaways

- Built a real-time SOC dashboard from scratch.
- Learned how to detect and visualize live threats using Splunk SPL.
- Simulated real-world attack scenarios (brute-force, web enumeration, failed logins).
- Gained experience in log analysis, correlation, and data visualization.

# Expansion: Sysmon and Advanced Detection
- Installed and configured Sysmon64 with a custom XML config to log process creation, network connections, and registry modifications.
- Verified logging under Microsoft-Windows-Sysmon/Operational and ingested into Splunk via XmlWinEventLog.
Added three new detections:
- PowerShell Abuse (EventCode 1)
- Suspicious Network Connections (EventCode 3)
- Persistence via Registry Modifications (EventCode 13)
Integrated all detections into the Threat Dashboard with live auto-refresh.
Demonstrated real-time detection by simulating benign and malicious activities.
