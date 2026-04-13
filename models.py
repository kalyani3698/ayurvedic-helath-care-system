from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'email': self.email,
            'age': self.age, 'gender': self.gender,
            'height': self.height, 'weight': self.weight,
            'createdAt': self.created_at.isoformat()
        }

class HealthData(db.Model):
    __tablename__ = 'health_data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sleep_hours = db.Column(db.Float)
    exercise_frequency = db.Column(db.String(50))
    work_type = db.Column(db.String(50))
    stress_level = db.Column(db.String(50))
    current_symptoms = db.Column(db.Text)
    existing_diseases = db.Column(db.Text)
    digestive_health = db.Column(db.String(100))
    food_habits = db.Column(db.String(100))
    water_intake = db.Column(db.Float)
    energy_level = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'userId': self.user_id,
            'sleepHours': self.sleep_hours, 'exerciseFrequency': self.exercise_frequency,
            'workType': self.work_type, 'stressLevel': self.stress_level,
            'currentSymptoms': self.current_symptoms, 'existingDiseases': self.existing_diseases,
            'digestiveHealth': self.digestive_health, 'foodHabits': self.food_habits,
            'waterIntake': self.water_intake, 'energyLevel': self.energy_level,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

class DoshaResult(db.Model):
    __tablename__ = 'dosha_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dominant_dosha = db.Column(db.String(20), nullable=False)
    vata_score = db.Column(db.Float, nullable=False)
    pitta_score = db.Column(db.Float, nullable=False)
    kapha_score = db.Column(db.Float, nullable=False)
    health_tendencies = db.Column(db.Text)
    recommended_diet = db.Column(db.Text)
    lifestyle_advice = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'userId': self.user_id,
            'dominantDosha': self.dominant_dosha,
            'vataScore': self.vata_score, 'pittaScore': self.pitta_score,
            'kaphaScore': self.kapha_score,
            'healthTendencies': self.health_tendencies,
            'recommendedDiet': self.recommended_diet,
            'lifestyleAdvice': self.lifestyle_advice,
            'analyzedAt': self.analyzed_at.isoformat()
        }

class SymptomRecord(db.Model):
    __tablename__ = 'symptom_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    possible_causes = db.Column(db.Text)
    natural_remedies = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'userId': self.user_id,
            'symptoms': self.symptoms, 'possibleCauses': self.possible_causes,
            'naturalRemedies': self.natural_remedies,
            'analyzedAt': self.analyzed_at.isoformat()
        }

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'userId': self.user_id,
            'role': self.role, 'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
