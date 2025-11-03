# Defending Against Multi-Stage Phishing Attack
**Fictional Case Study for Portfolio Demonstration Purposes**

### Key Competencies
- Incident Detection & Response (SIEM + EDR)
- Threat Hunting & IOC Analysis
- Phishing Investigation & Email Security
- Endpoint Containment & Network Blocking
- Clear Communication & Cross-Team Coordination

### Summary
This case study demonstrates how I responded as a Tier 1 SOC Analyst during a multi-stage phishing campaign that leveraged **PowerShell, Pastebin, and Telegram-based C2 channels**. My focus: detect the threat early, contain it quickly, investigate thoroughly, and ensure it could not return.

## Incident Overview
A phishing campaign targeted multiple departments, attempting to execute a **PowerShell loader** that pulled malicious scripts from **Pastebin**, with a fallback **Telegram API C2** channel. The attacker’s likely objective: **establish foothold → deploy second-stage payload → enable ransomware or remote access.** My responsibilities included alert triage, host containment, IOC development, enterprise hunting, and coordination with Tier 2 for deeper forensic and recovery actions.

## Detection & Triage
The first alert I investigated showed:
- `powershell.exe -nop -w hidden`
- `DownloadString()` to a raw Pastebin URL

This immediately indicated a high-risk, script-based malware attempt. At the same time, Proofpoint logs confirmed multiple phishing clicks, indicating a coordinated campaign.

I quickly:
- Pulled SIEM data to confirm scope
- Queried EDR to validate execution trails
- Identified impacted users and systems
- Prioritized hosts with confirmed script execution

## Containment Actions
To prevent escalation, I executed containment in layers:

**1. Endpoint Isolation**  
Isolated compromised machines through the EDR console to freeze malicious processes in place.

**2. Network Blocking**  
- Blocked the malicious Pastebin domain  
- Blocked Telegram API endpoints (fallback C2)

**3. Communication**  
Alerted affected users and managers to prevent re-infection and ensure no rebooting or tampering with live hosts.

These steps eliminated the attacker's ability to call home or spread laterally.

## Forensic Analysis & IOC Hunting
Before killing processes, I initiated a **RAM capture** on the primary infected host. Memory artifacts revealed:
- The Pastebin loader logic
- An AES-encrypted config blob
- Telegram API C2 references

I then:
- Extracted IOCs
- Conducted an enterprise-wide hunt in SIEM + EDR
- Verified **no persistence or lateral movement** beyond patient zero

## Eradication & Recovery
- Removed malicious scheduled tasks and PowerShell artifacts
- Ran full EDR scans to verify host integrity
- Forced **password resets and MFA re-enrollment for all users who clicked**
- Reconnected clean hosts to the network
- Assigned a short phishing awareness refresher

After a **72-hour monitoring window**, no further threats were observed and the incident was closed successfully.

## Outcome
- **No data exfiltration**
- **No ransomware execution**
- **No lateral movement**
- **Minimal business disruption**

Strong early detection and layered containment prevented what could have been a serious breach.

## Lessons Learned
- Multi-channel C2 is increasingly common (legitimate services abused for stealth)
- Memory capture before process kill can reveal critical evidence
- User awareness remains a crucial defense layer

## Skills Demonstrated
- Tools: Splunk (SIEM), CrowdStrike (EDR), Proofpoint, Firewall/Proxy controls
- Technical: PowerShell malware triage, IOC hunting, network containment, DFIR fundamentals
- Frameworks: MITRE ATT&CK, incident lifecycle (NIST), kill chain disruption
- Soft Skills: Communication, decision-making under pressure, cross-team collaboration

## Appendix A - MITRE ATT&CK Mapping
- **T1566.002** — Phishing (Link)
- **T1059.001** — PowerShell Execution
- **T1105 / T1071.001** — Web-based C2
- **T1053.005** — Scheduled Task Persistence

## Appendix B - Indicators of Compromise (IOCs)
- `https://pastebin.com/raw/...`
- `https://api.telegram.org/bot...`
- PowerShell pattern: `-nop -w hidden -c DownloadString()`

### Conclusion
This incident reflects how I approach cybersecurity: **focused, structured, calm under pressure, and driven by a layered defense mindset.** I follow a clear process:

> **Identify → Contain → Investigate → Eradicate → Recover → Improve**

My goal as a SOC Analyst is simple: **protect the organization, eliminate threats early, and continuously strengthen our defenses.**
