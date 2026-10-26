from flask import Flask
from flask_login import LoginManager
from models import db, User
from auth import auth_bp
from routes import routes_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-super-secret-key-change-this-in-production'
    
    # Use /tmp for Vercel's read-only filesystem
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/glaucoma.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    os.makedirs('/tmp/uploads', exist_ok=True)
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(routes_bp)
    
    with app.app_context():
        db.create_all()
        print("✅ Database created/verified.")
    
    return app

# 🔥 THIS IS THE CRITICAL LINE VERCEL NEEDS 🔥
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)