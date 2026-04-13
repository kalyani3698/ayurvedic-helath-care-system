from flask import Blueprint, jsonify

knowledge_bp = Blueprint('knowledge', __name__)

DOSHAS = [
    {'name': 'Vata', 'elements': 'Air & Ether (Space)', 'qualities': 'Light, Dry, Cold, Rough, Subtle, Mobile',
     'description': 'Vata is the principle of movement and governs all motion in the body and mind. It controls breathing, blinking, muscle movement, heartbeat, and all nerve impulses.',
     'healthTendencies': 'Anxiety, insomnia, dry skin, constipation, joint pain, irregular digestion, fluctuating energy',
     'balancingFoods': 'Warm soups, cooked grains, dairy, nuts, sesame oil, sweet fruits, warming spices like ginger and cinnamon',
     'avoidFoods': 'Raw vegetables, cold drinks, beans (except mung), dry foods, caffeine, alcohol',
     'lifestyleTips': 'Regular routine, warm oil massage, gentle yoga, adequate sleep, stay warm, avoid overexertion', 'color': 'blue'},
    {'name': 'Pitta', 'elements': 'Fire & Water', 'qualities': 'Hot, Sharp, Light, Oily, Liquid, Spreading',
     'description': 'Pitta governs transformation, digestion, and metabolism. It controls the digestion of food, thoughts, and experiences, and regulates body temperature.',
     'healthTendencies': 'Inflammation, acidity, skin rashes, irritability, excessive hunger, perfectionism, early graying',
     'balancingFoods': 'Sweet fruits, leafy greens, coconut, dairy, whole grains, cooling herbs like coriander and fennel',
     'avoidFoods': 'Spicy foods, sour fruits, alcohol, red meat, caffeine, fermented foods, excess salt',
     'lifestyleTips': 'Avoid excess heat and sun, cooling exercise like swimming, moonlit walks, cultivate patience, coconut oil massage', 'color': 'orange'},
    {'name': 'Kapha', 'elements': 'Earth & Water', 'qualities': 'Heavy, Slow, Cool, Oily, Smooth, Dense, Soft, Stable',
     'description': 'Kapha provides structure, stability, and lubrication. It governs growth, immunity, and the body\'s physical form, maintaining fluids and protecting tissues.',
     'healthTendencies': 'Weight gain, congestion, lethargy, depression, attachment, slow metabolism, excessive sleep',
     'balancingFoods': 'Light grains, legumes, vegetables, spicy herbs, honey, warm beverages, pungent and bitter tastes',
     'avoidFoods': 'Heavy foods, dairy, fried foods, sweets, cold drinks, processed foods, excessive meat',
     'lifestyleTips': 'Vigorous daily exercise, early rising, avoid daytime sleep, dry brushing, seek new experiences, stay socially active', 'color': 'green'},
]

HERBS = [
    {'name': 'Ashwagandha', 'sanskritName': 'Withania somnifera', 'benefits': 'Reduces stress and anxiety, boosts immunity, improves strength and stamina', 'uses': 'Stress relief, energy boost, immunity, sleep improvement', 'doshaEffect': 'Balances Vata and Kapha', 'precautions': 'Avoid during pregnancy'},
    {'name': 'Turmeric', 'sanskritName': 'Curcuma longa', 'benefits': 'Powerful anti-inflammatory, antioxidant, supports digestion and liver health', 'uses': 'Inflammation, joint pain, digestive support, skin conditions', 'doshaEffect': 'Balances all three doshas', 'precautions': 'May thin blood; consult doctor if on blood thinners'},
    {'name': 'Brahmi', 'sanskritName': 'Bacopa monnieri', 'benefits': 'Enhances memory and cognitive function, reduces anxiety, promotes hair growth', 'uses': 'Brain health, memory, anxiety, hair nourishment', 'doshaEffect': 'Balances Vata and Pitta', 'precautions': 'May cause digestive issues in excess'},
    {'name': 'Triphala', 'sanskritName': 'Amalaki, Bibhitaki, Haritaki', 'benefits': 'Powerful digestive tonic, antioxidant, supports colon health and detoxification', 'uses': 'Constipation, digestion, detox, eye health', 'doshaEffect': 'Balances all three doshas', 'precautions': 'Start with small doses; not recommended during pregnancy'},
    {'name': 'Neem', 'sanskritName': 'Azadirachta indica', 'benefits': 'Purifies blood, treats skin disorders, antibacterial, antifungal', 'uses': 'Skin conditions, blood purification, dental health, immunity', 'doshaEffect': 'Balances Pitta and Kapha', 'precautions': 'Avoid long-term use'},
    {'name': 'Tulsi', 'sanskritName': 'Ocimum sanctum', 'benefits': 'Adaptogenic, immune-boosting, respiratory support, stress relief, antibacterial', 'uses': 'Colds, stress, respiratory issues, fever, immunity', 'doshaEffect': 'Balances Vata and Kapha', 'precautions': 'May thin blood'},
    {'name': 'Ginger', 'sanskritName': 'Zingiber officinale', 'benefits': 'Stimulates digestion, anti-nausea, anti-inflammatory, warming, promotes circulation', 'uses': 'Nausea, indigestion, cold, inflammation, circulation', 'doshaEffect': 'Balances Vata and Kapha', 'precautions': 'Avoid in large amounts with Pitta conditions'},
]

PRODUCTS = [
    {'name': 'Patanjali Ashwagandha Capsules', 'store': 'Patanjali', 'url': 'https://www.patanjaliayurved.net', 'category': 'Immunity & Vitality', 'description': 'Herbal supplement for stress and immunity'},
    {'name': 'Organic Triphala Churna', 'store': 'Amazon India', 'url': 'https://www.amazon.in/s?k=organic+triphala+churna', 'category': 'Digestive Health', 'description': 'Traditional Ayurvedic digestive tonic'},
    {'name': 'Brahmi Hair Oil', 'store': 'Amazon India', 'url': 'https://www.amazon.in/s?k=brahmi+hair+oil', 'category': 'Hair & Brain Health', 'description': 'Nourishing oil for hair and cognitive health'},
    {'name': 'Chyawanprash Special', 'store': 'Patanjali', 'url': 'https://www.patanjaliayurved.net', 'category': 'Immunity', 'description': 'Classic herbal jam for immunity and vitality'},
    {'name': 'Neem Face Wash', 'store': 'Tata 1mg', 'url': 'https://www.1mg.com/search/all?name=neem+face+wash', 'category': 'Skin Care', 'description': 'Natural neem for clear, healthy skin'},
    {'name': 'Tulsi Green Tea', 'store': 'Organic India', 'url': 'https://www.organicindia.com/collections/tulsi-teas', 'category': 'Wellness Teas', 'description': 'Adaptogenic holy basil for daily wellness'},
    {'name': 'Shatavari Powder', 'store': 'Amazon India', 'url': 'https://www.amazon.in/s?k=shatavari+powder', 'category': 'Women\'s Health', 'description': 'Rejuvenating herb for hormonal balance'},
    {'name': 'Turmeric Capsules', 'store': 'Tata 1mg', 'url': 'https://www.1mg.com/search/all?name=turmeric+capsules', 'category': 'Anti-inflammatory', 'description': 'Curcumin supplement for joint and gut health'},
    {'name': 'Himalaya Herbal Healthcare', 'store': 'Himalaya', 'url': 'https://himalayawellness.in/collections/healthcare', 'category': 'General Ayurvedic', 'description': 'Wide range of Ayurvedic health products'},
]

@knowledge_bp.route('/doshas', methods=['GET'])
def doshas(): return jsonify(DOSHAS)

@knowledge_bp.route('/herbs', methods=['GET'])
def herbs(): return jsonify(HERBS)

@knowledge_bp.route('/products', methods=['GET'])
def products(): return jsonify(PRODUCTS)
