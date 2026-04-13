from flask import Blueprint, request, jsonify, session
from app import db
from models import ChatMessage
from groq import Groq
import os

chat_bp = Blueprint('chat', __name__)
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

SYSTEM_PROMPT = """You are an expert Ayurvedic health assistant with deep knowledge of traditional Indian medicine. You provide educational information about:
- Ayurvedic principles and the three doshas (Vata, Pitta, Kapha)
- Natural herbal remedies and their uses
- Ayurvedic diet recommendations and food guidelines
- Lifestyle practices for health and wellness
- Natural approaches to common health concerns

Always remind users that your advice is educational and they should consult a healthcare professional for medical conditions. Keep responses concise (2-4 paragraphs), practical, and grounded in Ayurvedic wisdom."""

@chat_bp.route('/message', methods=['POST'])
def message():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    history = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp.asc()).limit(20).all()
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    messages += [{'role': m.role, 'content': m.content} for m in history]
    messages.append({'role': 'user', 'content': user_message})

    try:
        completion = groq_client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )
        assistant_message = completion.choices[0].message.content or 'I could not generate a response. Please try again.'
    except Exception as e:
        assistant_message = f'Error: {str(e)[:100]}'

    db.session.add(ChatMessage(user_id=user_id, role='user', content=user_message))
    db.session.add(ChatMessage(user_id=user_id, role='assistant', content=assistant_message))
    db.session.commit()

    from datetime import datetime
    return jsonify({'userMessage': user_message, 'assistantMessage': assistant_message, 'timestamp': datetime.utcnow().isoformat()})

@chat_bp.route('/history', methods=['GET'])
def history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp.asc()).limit(100).all()
    return jsonify([m.to_dict() for m in messages])
