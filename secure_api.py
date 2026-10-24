
import hashlib
import json
import time
import os
from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

# --- CONFIGURATION ---
MODEL_PATH = 'best_glaucoma_final.keras'  # Place this in the same folder
THRESHOLD = 0.55345434
API_KEY = "Glaucoma_Project_2026_Secret_Key"

# --- LOAD MODEL ---
print("🔄 Loading model...")
model = load_model(MODEL_PATH)
print("✅ Model loaded!")

def anonymize_patient_id(patient_id):
    return hashlib.sha256(str(patient_id).encode()).hexdigest()

def predict_glaucoma(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prob = model.predict(img_array, verbose=0)[0][0]
    pred = 1 if prob >= THRESHOLD else 0
    return pred, float(prob)

app = Flask(__name__)
AUDIT_FILE = 'audit_log.json'

@app.route('/')
def home():
    return jsonify({"service": "Glaucoma Detection API", "status": "running", "threshold": THRESHOLD})

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Authentication (Bouncer)
    key = request.headers.get('X-API-Key')
    if not key or key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
    # 2. Get Data
    data = request.get_json()
    if not data or 'patient_id' not in data or 'image_path' not in data:
        return jsonify({"error": "Missing patient_id or image_path"}), 400
    
    patient_id = data['patient_id']
    image_path = data['image_path']
    
    # 3. Anonymization (Mask)
    hashed_id = anonymize_patient_id(patient_id)
    
    try:
        # 4. Predict
        pred_class, prob = predict_glaucoma(image_path)
        
        # 5. Audit Log (CCTV)
        log_entry = {
            "timestamp": time.time(),
            "hashed_patient_id": hashed_id,
            "prediction": int(pred_class),
            "probability": prob,
            "threshold": THRESHOLD
        }
        with open(AUDIT_FILE, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
        
        # 6. Response
        return jsonify({
            "hashed_patient_id": hashed_id,
            "prediction": "Glaucoma Detected" if pred_class == 1 else "Healthy",
            "probability": prob,
            "threshold": THRESHOLD,
            "timestamp": time.time()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
