from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index(): return render_template('index.html')

@pages_bp.route('/login')
def login(): return render_template('login.html')

@pages_bp.route('/register')
def register(): return render_template('register.html')

@pages_bp.route('/dashboard')
def dashboard(): return render_template('dashboard.html')

@pages_bp.route('/health-data')
def health_data(): return render_template('health_data.html')

@pages_bp.route('/dosha-quiz')
def dosha_quiz(): return render_template('dosha_quiz.html')

@pages_bp.route('/symptom-analyzer')
def symptom_analyzer(): return render_template('symptom_analyzer.html')

@pages_bp.route('/chat')
def chat(): return render_template('chat.html')

@pages_bp.route('/knowledge')
def knowledge(): return render_template('knowledge.html')
