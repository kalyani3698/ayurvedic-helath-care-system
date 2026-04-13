from flask import Blueprint, request, jsonify, session
from app import db
from models import SymptomRecord
from groq import Groq
import os, json, re

symptoms_bp = Blueprint('symptoms', __name__)
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

PRODUCTS = [
    {'name': 'Triphala Churna', 'store': 'Amazon', 'url': 'https://www.amazon.in/s?k=triphala+churna', 'category': 'Digestive Health', 'description': 'Classic Ayurvedic digestive tonic'},
    {'name': 'Ashwagandha Capsules', 'store': 'Patanjali', 'url': 'https://www.patanjaliayurved.net', 'category': 'Stress & Immunity', 'description': 'Adaptogenic herb for stress relief'},
    {'name': 'Brahmi Oil', 'store': 'Tata 1mg', 'url': 'https://www.1mg.com/search/all?name=brahmi+oil', 'category': 'Brain Health', 'description': 'Nourishing hair and brain tonic'},
    {'name': 'Neem Tablets', 'store': 'Organic India', 'url': 'https://www.organicindia.com', 'category': 'Skin Health', 'description': 'Purifying herb for skin and blood'},
    {'name': 'Chyawanprash', 'store': 'Amazon', 'url': 'https://www.amazon.in/s?k=chyawanprash', 'category': 'Immunity', 'description': 'Herbal jam for immunity and vitality'},
    {'name': 'Turmeric Capsules', 'store': 'Tata 1mg', 'url': 'https://www.1mg.com/search/all?name=turmeric', 'category': 'Anti-inflammatory', 'description': 'Curcumin for inflammation and joints'},
]

def select_products(symptoms, remedies):
    text = (symptoms + ' ' + remedies).lower()
    result = []
    if any(w in text for w in ['digest', 'stomach', 'bowel', 'bloat', 'constip']): result.append(PRODUCTS[0])
    if any(w in text for w in ['stress', 'anxiet', 'fatigue', 'immune', 'weak']): result.extend([PRODUCTS[1], PRODUCTS[4]])
    if any(w in text for w in ['head', 'brain', 'focus', 'memor', 'hair']): result.append(PRODUCTS[2])
    if any(w in text for w in ['skin', 'acne', 'rash', 'itch']): result.append(PRODUCTS[3])
    if any(w in text for w in ['inflam', 'joint', 'pain', 'arthrit']): result.append(PRODUCTS[5])
    if not result: result = [PRODUCTS[1], PRODUCTS[4]]
    seen, unique = set(), []
    for p in result:
        if p['name'] not in seen:
            seen.add(p['name'])
            unique.append(p)
    return unique[:3]

@symptoms_bp.route('/analyze', methods=['POST'])
def analyze():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.get_json()
    symptoms = data.get('symptoms', '').strip()
    if not symptoms:
        return jsonify({'error': 'Symptoms are required'}), 400
    duration = data.get('duration', '')
    severity = data.get('severity', '')

    prompt = f'''You are an expert Ayurvedic practitioner. A patient reports symptoms: "{symptoms}"{f", lasting {duration}" if duration else ""}{f", severity: {severity}" if severity else ""}.

Provide a comprehensive Ayurvedic analysis in JSON format with exactly these keys:
{{"possibleCauses": "...", "ayurvedicExplanation": "...", "naturalRemedies": "...", "dietSuggestions": "...", "lifestyleImprovements": "..."}}

Be specific, practical, and educational. Focus on Ayurvedic principles. Keep each field to 2-3 sentences.'''

    try:
        completion = groq_client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7, max_tokens=800
        )
        content = completion.choices[0].message.content or '{}'
        match = re.search(r'\{[\s\S]*\}', content)
        analysis = json.loads(match.group()) if match else {}
    except Exception as e:
        analysis = {'possibleCauses': 'Analysis unavailable.', 'ayurvedicExplanation': str(e)[:100],
                    'naturalRemedies': 'Consult an Ayurvedic practitioner.',
                    'dietSuggestions': 'Follow a balanced Ayurvedic diet.',
                    'lifestyleImprovements': 'Practice yoga and meditation daily.'}

    remedies = analysis.get('naturalRemedies', '')
    record = SymptomRecord(user_id=user_id, symptoms=symptoms,
                           possible_causes=analysis.get('possibleCauses'),
                           natural_remedies=remedies)
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'symptoms': symptoms,
        'possibleCauses': analysis.get('possibleCauses', ''),
        'ayurvedicExplanation': analysis.get('ayurvedicExplanation', ''),
        'naturalRemedies': remedies,
        'dietSuggestions': analysis.get('dietSuggestions', ''),
        'lifestyleImprovements': analysis.get('lifestyleImprovements', ''),
        'relatedProducts': select_products(symptoms, remedies)
    })

@symptoms_bp.route('/history', methods=['GET'])
def history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    records = SymptomRecord.query.filter_by(user_id=user_id).order_by(SymptomRecord.analyzed_at.desc()).limit(20).all()
    return jsonify([r.to_dict() for r in records])
