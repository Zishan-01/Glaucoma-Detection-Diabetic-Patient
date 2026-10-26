import gradio as gr
import numpy as np
from PIL import Image
from model_loader import predict_glaucoma # Assuming this is your prediction function
from flask import Flask

# 1. Initialize your Flask app (if you have one, import it)
# If your Flask app is in another file, import it here. Otherwise, just use a dummy.
flask_app = Flask(__name__)

# 2. Define the prediction function for Gradio
def predict_image(image):
    if image is None:
        return "Please upload an image."
    
    # Save the uploaded image temporarily so your model can read it
    temp_path = "temp_upload.jpg"
    image.save(temp_path)
    
    # Call your existing AI logic
    result = predict_glaucoma(temp_path) 
    
    # Format the output nicely for the doctor
    diagnosis = result['prediction']
    confidence = result['confidence'] * 100
    
    return f"Diagnosis: {diagnosis}\nConfidence: {confidence:.2f}%"

# 3. Build the Gradio Interface
interface = gr.Interface(
    fn=predict_image,
    inputs=gr.Image(type="pil", label="Upload Fundus Image"),
    outputs=gr.Textbox(label="AI Prediction Result"),
    title="👁️ Glaucoma Detection in Diabetic Patients",
    description="Upload a fundus image to get an AI-powered prediction. (Powered by MobileNetV2)",
    theme="soft"
)

# 4. Mount Gradio to Flask (This allows Hugging Face to host it)
app = gr.mount_gradio_app(flask_app, interface, path="/")

# 5. Run the app
if __name__ == "__main__":
    app.run(port=7860) # Hugging Face requires port 7860