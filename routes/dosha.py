from flask import Blueprint, request, jsonify, session
from app import db
from models import DoshaResult

dosha_bp = Blueprint('dosha', __name__)

def calculate_dosha(data):
    vata, pitta, kapha = 0, 0, 0
    sleep = float(data.get('sleepHours', 7) or 7)
    if sleep < 6: vata += 2
    elif sleep <= 8: pitta += 1
    else: kapha += 2

    stress = str(data.get('stressLevel', '')).lower()
    if stress in ['high', 'very high']: vata += 3
    elif stress in ['medium', 'moderate']: pitta += 2
    else: kapha += 1

    energy = str(data.get('energyLevel', '')).lower()
    if energy == 'low': vata += 2
    elif energy in ['high', 'very high']: pitta += 2
    else: kapha += 1

    digestive = str(data.get('digestiveHealth', '')).lower()
    if any(w in digestive for w in ['irregular', 'bloat', 'gas']): vata += 2
    elif any(w in digestive for w in ['acidity', 'heartburn', 'sharp']): pitta += 2
    elif any(w in digestive for w in ['slow', 'heavy', 'sluggish']): kapha += 2

    food = str(data.get('foodHabits', '')).lower()
    if any(w in food for w in ['irregular', 'raw', 'light']): vata += 1
    elif any(w in food for w in ['spicy', 'hot', 'sour']): pitta += 1
    else: kapha += 1

    exercise = str(data.get('exerciseFrequency', '')).lower()
    if any(w in exercise for w in ['rarely', 'never', 'low']): vata += 1
    elif any(w in exercise for w in ['daily', 'intense', 'high']): pitta += 1
    else: kapha += 1

    work = str(data.get('workType', '')).lower()
    if work == 'active': pitta += 1
    elif work == 'sedentary': kapha += 1

    total = vata + pitta + kapha or 1
    vata_pct = round((vata / total) * 100)
    pitta_pct = round((pitta / total) * 100)
    kapha_pct = 100 - vata_pct - pitta_pct

    if pitta >= vata and pitta >= kapha: dominant = 'Pitta'
    elif kapha >= vata and kapha >= pitta: dominant = 'Kapha'
    else: dominant = 'Vata'

    return dominant, vata_pct, pitta_pct, kapha_pct

DOSHA_INFO = {
    'Vata': {
        'tendencies': 'Tendency towards anxiety, irregular digestion, dry skin, light sleep, and creativity. You may experience fluctuating energy levels and be sensitive to cold and wind.',
        'diet': 'Favor warm, moist, oily, and grounding foods. Include warm soups, cooked grains, dairy, nuts, and natural sweeteners. Avoid raw vegetables, cold foods, caffeine, and dry or light foods.',
        'lifestyle': 'Maintain a regular daily routine. Practice gentle yoga, meditation, and grounding activities. Get adequate rest, avoid overexertion, and stay warm. Sesame oil massage (Abhyanga) is highly beneficial.'
    },
    'Pitta': {
        'tendencies': 'Tendency towards inflammation, acidity, intense emotions, sharp intellect, and strong digestion. You may experience heat sensitivity, skin rashes, and competitive nature.',
        'diet': 'Favor cool, sweet, bitter, and astringent foods. Include fresh fruits, leafy greens, dairy, and whole grains. Avoid spicy, sour, oily, and fermented foods, alcohol, and excess salt.',
        'lifestyle': 'Avoid excessive heat and sun exposure. Practice cooling exercises like swimming and moonlit walks. Cultivate patience and compassion. Coconut oil massage is beneficial.'
    },
    'Kapha': {
        'tendencies': 'Tendency towards weight gain, lethargy, congestion, stable emotions, and strong endurance. You may experience slow metabolism, attachment, and need for motivation.',
        'diet': 'Favor light, warm, spicy, and stimulating foods. Include legumes, vegetables, spicy herbs, and light grains. Avoid heavy, oily, sweet, and cold foods, dairy excess, and processed foods.',
        'lifestyle': 'Engage in vigorous daily exercise. Wake up early and avoid daytime sleeping. Seek variety and new experiences. Dry brushing and invigorating massage are beneficial.'
    }
}

@dosha_bp.route('/analyze', methods=['POST'])
def analyze():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.get_json()
    dominant, vata_pct, pitta_pct, kapha_pct = calculate_dosha(data)
    info = DOSHA_INFO[dominant]
    result = DoshaResult.query.filter_by(user_id=user_id).first()
    if result:
        result.dominant_dosha = dominant
        result.vata_score = vata_pct
        result.pitta_score = pitta_pct
        result.kapha_score = kapha_pct
        result.health_tendencies = info['tendencies']
        result.recommended_diet = info['diet']
        result.lifestyle_advice = info['lifestyle']
    else:
        result = DoshaResult(user_id=user_id, dominant_dosha=dominant,
                             vata_score=vata_pct, pitta_score=pitta_pct,
                             kapha_score=kapha_pct, health_tendencies=info['tendencies'],
                             recommended_diet=info['diet'], lifestyle_advice=info['lifestyle'])
        db.session.add(result)
    db.session.commit()
    return jsonify(result.to_dict())

@dosha_bp.route('/result', methods=['GET'])
def get_result():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    result = DoshaResult.query.filter_by(user_id=user_id).order_by(DoshaResult.analyzed_at.desc()).first()
    if not result:
        return jsonify({'error': 'No dosha analysis found'}), 404
    return jsonify(result.to_dict())
