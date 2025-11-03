import cv2
import os
from datetime import datetime

# Create output directory 
OUTPUT_FOLDER = "captured_frames"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Starts the webcam
cap = cv2.VideoCapture(0)

# First frame for reference
ret, prev_frame = cap.read()
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)

img_count = 1
print("(*) Surveillance system started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compute the absolute difference between the current frame and previous frame
    frame_diff = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if motion_detected:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_filename = os.path.join(OUTPUT_FOLDER, f"motion_{timestamp}_{img_count}.jpg")
        filepath = os.path.join(OUTPUT_FOLDER, img_filename)
        cv2.imwrite(img_filename, frame)
        print(f"(*) Motion detected! Image saved: {img_filename}")
        img_count += 1

    # Display the resulting frame
    cv2.imshow("Motion Detector", frame)


    # Update previous frame
    prev_frame = gray

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cap.release()
    cv2.destroyAllWindows()
    print("[!] Surveillance system stopped.")