from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ayurveda-secret-key-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ayurveda.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Fix session/cookie settings for local development
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set True only for HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    db.init_app(app)
    bcrypt.init_app(app)

    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.dosha import dosha_bp
    from routes.symptoms import symptoms_bp
    from routes.chat import chat_bp
    from routes.knowledge import knowledge_bp
    from routes.pages import pages_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(dosha_bp, url_prefix='/api/dosha')
    app.register_blueprint(symptoms_bp, url_prefix='/api/symptoms')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
