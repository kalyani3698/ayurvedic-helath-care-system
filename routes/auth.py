from flask import Blueprint, request, jsonify, session
from app import db, bcrypt
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not name or not email or not password:
        return jsonify({'error': 'Name, email and password are required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name=name, email=email, password=hashed,
                age=data.get('age') or None, gender=data.get('gender') or None,
                height=data.get('height') or None, weight=data.get('weight') or None)
    db.session.add(user)
    db.session.commit()
    session.permanent = True
    session['user_id'] = user.id
    return jsonify({'user': user.to_dict(), 'message': 'Registration successful'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    session.permanent = True
    session['user_id'] = user.id
    return jsonify({'user': user.to_dict(), 'message': 'Login successful'})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 401
    return jsonify(user.to_dict())
