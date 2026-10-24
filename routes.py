from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, Report, User
from model_loader import predict_glaucoma

routes_bp = Blueprint('routes', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        flash('Access denied. Doctors only.', 'danger')
        return redirect(url_for('routes.index'))
    
    reports = Report.query.order_by(Report.created_at.desc()).all()
    patients = User.query.filter_by(role='patient').all()
    
    total_reports = len(reports)
    glaucoma_count = Report.query.filter_by(prediction='Glaucoma').count()
    healthy_count = Report.query.filter_by(prediction='Healthy').count()
    
    return render_template('doctor_dashboard.html', 
                         reports=reports, 
                         patients=patients,
                         total_reports=total_reports,
                         glaucoma_count=glaucoma_count,
                         healthy_count=healthy_count)

@routes_bp.route('/patient/dashboard')
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        flash('Access denied. Patients only.', 'danger')
        return redirect(url_for('routes.index'))
    
    reports = Report.query.filter_by(patient_id=current_user.id).order_by(Report.created_at.desc()).all()
    total = len(reports)
    glaucoma = sum(1 for r in reports if r.prediction == 'Glaucoma')
    healthy = total - glaucoma
    
    return render_template('patient_dashboard.html', 
                         reports=reports,
                         total=total,
                         glaucoma=glaucoma,
                         healthy=healthy)

@routes_bp.route('/doctor/upload', methods=['GET', 'POST'])
@login_required
def upload_report():
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('routes.index'))
    
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        notes = request.form.get('notes', '')
        
        if 'image' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, unique_filename)
            file.save(filepath)
            
            try:
                result = predict_glaucoma(filepath)
                
                new_report = Report(
                    patient_id=patient_id,
                    doctor_id=current_user.id,
                    image_filename=unique_filename,
                    prediction=result['prediction'],
                    probability=result['probability'],
                    confidence=result['confidence'],
                    severity_notes=notes
                )
                db.session.add(new_report)
                db.session.commit()
                
                flash(f'Report uploaded! AI says: {result["prediction"]} (Confidence: {result["confidence"]:.2%})', 'success')
                return redirect(url_for('routes.doctor_dashboard'))
            except Exception as e:
                flash(f'AI Error: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            flash('File type not allowed.', 'danger')
    
    patients = User.query.filter_by(role='patient').all()
    return render_template('upload_report.html', patients=patients)

@routes_bp.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    report = Report.query.get_or_404(report_id)
    if current_user.role == 'patient' and report.patient_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('routes.patient_dashboard'))
    return render_template('report_detail.html', report=report)

@routes_bp.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_' + filename)
    file.save(temp_path)
    result = predict_glaucoma(temp_path)
    os.remove(temp_path)
    return jsonify(result)