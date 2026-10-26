# Deepfake Image Detector
- A Convolutional Neural Network (CNN)-based deepfake detector that distinguishes between **real** (authentic) and **fake** (AI-generated) images.  
- Built for cybersecurity awareness and AI safety, this project uses image classification to help flag manipulated content.

# Overview
Trained on a small dataset of 18 labeled images (10 authentic, 8 synthetic), the model can:
- Determine whether an individual image is AI-generated.
- Run batch predictions by scanning an entire folder of images at once.
- Use a live webcam feed to detect deepfakes in real time.
- Display confidence scores alongside each prediction.

# Project Structure
```
DEEPFAKE_IMAGE_DETECTOR/
├── batch_predict.py   # Scans a folder of images and scores each one REAL or FAKE
├── predictions.csv    # Sample output from a batch run
└── README.md
```

> **Dataset not included.** The training images were removed from this repo for privacy. To run the project, add your own images to `dataset/real/` and `dataset/fake/` (public sets such as the Kaggle "140k Real and Fake Faces" dataset work well). The training script, webcam script, and saved model are not yet published.

# Features
- Binary classification (REAL vs FAKE)
- CNN architecture: Conv2D, MaxPooling, Dense, Dropout
- Transfer learning with VGG16 for improved accuracy
- Batch prediction for entire folders
- Live webcam detection (flags and saves fake frames)
- Confidence scores (e.g., REAL - 92%)

# How it works (full pipeline)

1. **Train the model** — image augmentation plus VGG16 transfer learning; the model is saved as `saved_model.h5`.
2. **Batch predict** — set `INPUT_PATH` in `batch_predict.py` to a folder of images and run `python batch_predict.py`. Each image gets a REAL/FAKE label and confidence score, written to `predictions.csv`.
3. **Live webcam detection** — scores webcam frames in real time and saves suspected fakes to `flagged_fakes/`.

# Requirements

- Python 3
- TensorFlow / Keras
- NumPy
- OpenCV
- Pillow (PIL)

# Notes
- The dataset is very small, so accuracy will vary. A larger public dataset would improve results.

# Author
Prabhdeep Dhillon — CompTIA Security+ · B.S. Cybersecurity, DePaul University
