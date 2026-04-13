================================================
  AYURVEDIC HEALTHCARE SYSTEM - Flask Version
================================================

SETUP INSTRUCTIONS FOR VS CODE
--------------------------------

REQUIREMENTS:
  - Python 3.9 or higher
  - VS Code with Python extension
  - Internet connection (for Groq AI API)

STEP 1 - Install Python
  Download from: https://www.python.org/downloads/
  Make sure to check "Add Python to PATH" during install.

STEP 2 - Open Project in VS Code
  File → Open Folder → Select the "ayurveda-flask" folder

STEP 3 - Create a virtual environment
  Open the VS Code terminal (Ctrl+` or View → Terminal) and run:
    python -m venv venv

STEP 4 - Activate the virtual environment
  On Windows:
    venv\Scripts\activate
  On Mac/Linux:
    source venv/bin/activate

STEP 5 - Install dependencies
  pip install -r requirements.txt

STEP 6 - Configure your API key
  Open the .env file and replace:
    GROQ_API_KEY=your_groq_api_key_here
  with your actual Groq API key.

  You can get a free Groq API key at: https://console.groq.com

STEP 7 - Run the application
  python app.py

STEP 8 - Open in browser
  Go to: http://127.0.0.1:5000

================================================

PROJECT STRUCTURE:
  app.py              - Main Flask application
  models.py           - Database models (SQLite)
  routes/
    auth.py           - Login, Register, Logout
    user.py           - Health data input/retrieval
    dosha.py          - Dosha analysis algorithm
    symptoms.py       - AI-powered symptom analyzer
    chat.py           - AI health assistant chat
    knowledge.py      - Knowledge base (doshas, herbs, products)
    pages.py          - HTML page routes
  templates/          - HTML pages
  static/
    css/style.css     - All styling
    js/main.js        - Frontend JavaScript
  .env                - Your API keys (do not share this file)

================================================

DATABASE:
  The app uses SQLite — no setup needed.
  A file "ayurveda.db" will be automatically created
  when you first run the app.

================================================

FEATURES:
  ✅ User Registration & Login
  ✅ Health Data Input (lifestyle + symptoms)
  ✅ Dosha Quiz (Vata / Pitta / Kapha detection)
  ✅ AI Symptom Analyzer (powered by Groq AI)
  ✅ AI Health Chat Assistant
  ✅ Digital Twin Dashboard
  ✅ Ayurvedic Knowledge Base
  ✅ Ayurvedic Product Store Links

================================================
