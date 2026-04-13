# 🌿 AyurVeda Flask App - Setup Guide

## How to Run Locally (College / Any PC)

### Step 1: Install Python
Make sure Python 3.8+ is installed. Check with:
```
python --version
```

### Step 2: Install Dependencies
Open terminal/command prompt in this folder and run:
```
pip install -r requirements.txt
```

### Step 3: (Optional) Add Groq API Key
Open the `.env` file and replace `your_groq_api_key_here` with your real key.
Get a FREE key from: https://console.groq.com

The app works without it — the AI Chat feature just won't respond.

### Step 4: Run the App
```
python run.py
```

### Step 5: Open in Browser
Go to: **http://localhost:5000**

---

## Troubleshooting

- **"Connection error. Please try again."** — This was a Replit-specific issue. It is now FIXED.
- **ModuleNotFoundError** — Run `pip install -r requirements.txt` again.
- **Port already in use** — Change port in run.py from `5000` to `5001`.
