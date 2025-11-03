# Overview
This project is the development of a real-time motion detection system using Python and OpenCV. The system continuously captures video from a webcam, detects motion by capturing frames, and automatically saves timestamped snapshots when movement occurs.
It's lightweight yet powerful example of computer vision in physical security, built to run on both Raspberry Pi and desktop computers.

# Features
- Live video capture from webcam.
- Motion detection using frame differencing and thresholding.
- Visual feedback that highlights detected movement. 
- Automatic snapshot saving when motion is detected. 
- Timestamping for evidence and review. 
- Compatible with MacOS, Windows, Linux, and Raspberry Pi

# Technologies
- Python3
- OpenCV (cv2)
- datetime
- os

# Project Structure
motion_detection_system/
│── motion_detector.py        # Main motion detection script
│── captured_frames/          # Stores saved motion snapshots
│── README.md                 # Project Documentation 

#  How It Works
- Webcam Integration - The script connects to your webcam using OpenCV
- Frame Comparison - Each new frame is compared to previous one to detect visual differences. 
- Motion Detection Logic - When significant change is found, it is treated as motion. 
- Snapshot Saving - A still image is saved automatically with a timestamp for record keeping.
- User Control - Press 'q' anytime to stop the surveillance system safely.

# What I Learned
- OpenCV Basics: Captured and processed live video feeds
- Motion Detection: Detected movement via frame differencing
- Image Saving: Stored frames when motion occurred
- File Handling: Created and managed timestamped evidence. 
- Physical Security: Applied digital detection to real-world sureillance

# Why It Matters
This project brides AI and physical security, showing how computer vision can monitor real environments for activity. it's a foundational exercise for:
- Entry-Level Computer Vision: Working with live video feeds and frame analysis. 
- IoT-Based Security Applications: embedding AI-driven monitoring into connected systems.
- Smart Home or Surveillance Bot Development: adapting the same logic for patrol or smart camera systems.
- AI Integration: Extending this base for facial recognition or automated alerts. 

# Run It Yourself
1. Install OpenCV
- pip install opencv-python
2. Run the monitor detector
- python motion_detector.py
