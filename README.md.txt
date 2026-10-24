# 👁️ Glaucoma Detection in Diabetic Patients

An end-to-end, AI-powered clinical decision support system designed to detect Glaucoma in diabetic patients. This project integrates Deep Learning (AIML), Data Visualization (DAV), and Information Security (INS).

## 🚀 Key Features
- **Custom AI Model**: Fine-tuned MobileNetV2 trained exclusively on diabetic fundus images.
- **Clinical Safety First**: Achieved **100% Recall (Zero False Negatives)** using a custom threshold of 0.553.
- **Imbalance Handling**: Dual-mechanism of Class Weights (27.38) and Bias Initialization (-2.0) to overcome a 53:1 data imbalance.
- **Data Analytics (DAV)**: Interactive Power BI Dashboard analyzing risk based on Age, Sex, and Diabetic Retinopathy severity.
- **Information Security (INS)**: Secure Flask API with API-Key authentication, SHA-256 patient anonymization, and Audit Logging.
- **Role-Based Portal**: Dedicated web dashboards for Doctors (upload images/view analytics) and Patients (view personal reports).

## 🛠️ Tech Stack
- **Machine Learning**: TensorFlow, Keras, MobileNetV2, Scikit-Learn
- **Backend**: Python, Flask, SQLAlchemy, SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Data Visualization**: Power BI
- **Security**: SHA-256 Hashing, REST API Authentication

## 📂 Project Structure
```text
Glaucoma_Website/
│
├── app.py                # Main Flask application
├── models.py             # Database models (User, Report)
├── auth.py               # Login/Registration logic
├── routes.py             # Web URL endpoints
├── model_loader.py       # AI Model inference script
├── secure_api.py         # Standalone Secure REST API (INS)
├── requirements.txt      # Python dependencies
├── best_threshold.txt    # Optimized clinical threshold (0.553)
│
├── templates/            # HTML files for Web UI
└── static/               # CSS, JS, and Uploaded Images