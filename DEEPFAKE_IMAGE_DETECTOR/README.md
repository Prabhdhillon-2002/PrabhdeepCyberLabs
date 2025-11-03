# Deepfake Image Detector
- A Convolutional Neural Network (CNN)-based deepfake detector that distinguishes between **real** (authentic) and **fake** (AI-generated) images.  
- Built for cybersecurity awareness and AI safety, this project leverages image classification to help flag manipulated content.

# Overview
- Trained on a small dataset of 18 labeled images (10 authentic, 8 synthetic), the model is capable of:
- Determining whether an individual image is AI-generated.
- Performing batch predictions by scanning an entire folder of images at once.
- Utilizing a live webcam feed to detect deepfakes in real time.
- Displaying confidence scores alongside each prediction.

# Project Structure
deepfake_image_detector/
├── dataset/
│ ├── real/ # Contains authentic face images
│ └── fake/ # Contains AI-generated face images
├── mix/ # (Optional) Directory for mixed images used in batch prediction
├── train_model.py # Script to train and save the VGG16-based model
├── test_model.py # Used for predicting a single image or performing batch predictions
├── webcam_detector.py # Enables real-time deepfake detection via webcam
├── saved_model.h5 # The trained Keras model file
└── README.md # Project documentation (this file)

# Features
- Binary Classification (REAL vs FAKE)
- CNN architecture: Conv2D, MaxPooling, Dense, Dropout
- Transfer Learning with VGG16 for improved accuracy
- Batch prediction support for entire folders
- Live webcam detection (flags and saves fake frames)
- Confidence Scores (e.g., REAL - 92%)
- Clean and modular codebase

# How it works

1. Train the model
- Uses image augmentation and transfer learning with VGG16 to improve generalization.
- bash python train_model.py
- model is saved as saved_model.h5
2. Predict a single image or Folder 
- Open test_model.py and update the path: INPUT_PATH = "FOLDER/PICTURE"
- Run it python test_model.py
- Outputs prediction with confidence score for each image. 
3. Live Webcam Detection
- Predicts deepfakes in real time from your webcam.
- python webcam_detector.py
- If a fake frame is detected, it is saved to flagged_fakes/

# Requirements

- Python 3
- Tensorflow / Keras
- NumPy
- OpenCV
- Pillow (PIL)

# Notes
- Dataset size is small; accuracy may vary. Consider using larger datasets for improved accuracy.
- You can extend test_model.py to batch test multiple images and output predictions to CSV. 

# Author
Prabhdeep Dhillon
Cybersecurity Analyst
