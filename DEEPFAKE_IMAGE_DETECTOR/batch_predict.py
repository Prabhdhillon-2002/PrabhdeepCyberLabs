import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input  # ✅

MODEL_PATH = "saved_model.h5"
IMAGE_SIZE = (128, 128)
INPUT_PATH = "dataset/mix/"  # change to your test folder

# Load model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found at: {MODEL_PATH}")
model = load_model(MODEL_PATH)
print(f"✅ Model loaded from: {MODEL_PATH}")

# Predict function
def predict_image(img_path):
    img = load_img(img_path, target_size=IMAGE_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # ✅ VGG16 preprocessing

    pred = model.predict(img_array)[0][0]
    label = "REAL" if pred > 0.5 else "FAKE"
    confidence = pred if pred > 0.5 else 1 - pred

    print(f"[{os.path.basename(img_path)}] → {label} ({confidence:.2f})")

# Folder or file
if os.path.isfile(INPUT_PATH):
    predict_image(INPUT_PATH)

elif os.path.isdir(INPUT_PATH):
    files = [f for f in os.listdir(INPUT_PATH) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        print(f"⚠️ No images found in {INPUT_PATH}")
    else:
        print(f"🔍 Predicting {len(files)} image(s) in {INPUT_PATH}")
        for file in files:
            predict_image(os.path.join(INPUT_PATH, file))
else:
    print(f"❌ Path not found: {INPUT_PATH}")
