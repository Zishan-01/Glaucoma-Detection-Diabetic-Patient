from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reports = db.relationship('Report', backref='doctor', lazy=True, foreign_keys='Report.doctor_id')
    patient_reports = db.relationship('Report', backref='patient', lazy=True, foreign_keys='Report.patient_id')

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_filename = db.Column(db.String(200), nullable=False)
    prediction = db.Column(db.String(20), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    severity_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'image_filename': self.image_filename,
            'prediction': self.prediction,
            'probability': self.probability,
            'confidence': self.confidence,
            'severity_notes': self.severity_notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'patient_name': self.patient.full_name if self.patient else 'Unknown',
            'doctor_name': self.doctor.full_name if self.doctor else 'Unknown'
        }