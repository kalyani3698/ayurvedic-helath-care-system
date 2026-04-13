from flask import Blueprint, request, jsonify, session
from app import db
from models import HealthData
from datetime import datetime

user_bp = Blueprint('user', __name__)

def require_auth():
    user_id = session.get('user_id')
    if not user_id:
        return None, jsonify({'error': 'Not authenticated'}), 401
    return user_id, None, None

@user_bp.route('/health-data', methods=['GET'])
def get_health_data():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    data = HealthData.query.filter_by(user_id=user_id).first()
    if not data:
        return jsonify({'error': 'No health data found'}), 404
    return jsonify(data.to_dict())

@user_bp.route('/health-data', methods=['POST'])
def save_health_data():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    body = request.get_json()
    data = HealthData.query.filter_by(user_id=user_id).first()
    if data:
        data.sleep_hours = body.get('sleepHours')
        data.exercise_frequency = body.get('exerciseFrequency')
        data.work_type = body.get('workType')
        data.stress_level = body.get('stressLevel')
        data.current_symptoms = body.get('currentSymptoms')
        data.existing_diseases = body.get('existingDiseases')
        data.digestive_health = body.get('digestiveHealth')
        data.food_habits = body.get('foodHabits')
        data.water_intake = body.get('waterIntake')
        data.energy_level = body.get('energyLevel')
        data.updated_at = datetime.utcnow()
    else:
        data = HealthData(
            user_id=user_id,
            sleep_hours=body.get('sleepHours'),
            exercise_frequency=body.get('exerciseFrequency'),
            work_type=body.get('workType'),
            stress_level=body.get('stressLevel'),
            current_symptoms=body.get('currentSymptoms'),
            existing_diseases=body.get('existingDiseases'),
            digestive_health=body.get('digestiveHealth'),
            food_habits=body.get('foodHabits'),
            water_intake=body.get('waterIntake'),
            energy_level=body.get('energyLevel')
        )
        db.session.add(data)
    db.session.commit()
    return jsonify(data.to_dict())
