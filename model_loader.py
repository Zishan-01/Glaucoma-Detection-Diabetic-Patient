import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os

model = None
THRESHOLD = 0.553

def load_ai_model():
    global model, THRESHOLD
    if model is None:
        model_path = os.path.join(os.path.dirname(__file__), 'best_glaucoma_final.keras')
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            print("✅ AI Model loaded successfully!")
        else:
            raise FileNotFoundError("Model file not found!")
        
        threshold_path = os.path.join(os.path.dirname(__file__), 'best_threshold.txt')
        if os.path.exists(threshold_path):
            with open(threshold_path, 'r') as f:
                THRESHOLD = float(f.read().strip())
        print(f"✅ Threshold loaded: {THRESHOLD}")
    return model, THRESHOLD

def predict_glaucoma(image_path):
    model, threshold = load_ai_model()
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prob = model.predict(img_array, verbose=0)[0][0]
    pred_class = 1 if prob >= threshold else 0
    return {
        'prediction': 'Glaucoma' if pred_class == 1 else 'Healthy',
        'probability': float(prob),
        'confidence': float(max(prob, 1 - prob)),
        'threshold': float(threshold)
    }