# app.py (Render-ready version)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from google.cloud import texttospeech
import os
import base64

# -----------------------
# Setup Flask
# -----------------------
app = Flask(__name__)
CORS(app)

# -----------------------
# Configure Gemini API
# -----------------------
gemini_api_key = os.environ.get("AIzaSyDFV1gs4qVYnKtBRJO3jDp6rumNscYvbcI")
if not gemini_api_key:
    raise ValueError("Please set the GEMINI_API_KEY environment variable in Render.")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# -----------------------
# Setup Google TTS
# -----------------------
# Make sure you uploaded service-account.json as a Secret File in Render
# and set GOOGLE_APPLICATION_CREDENTIALS=/opt/render/project/secrets/service-account.json
tts_client = texttospeech.TextToSpeechClient()

# -----------------------
# Routes for HTML Pages
# -----------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/voice")
def voice_page():
    return render_template("voice.html")

# -----------------------
# API Route for Chat
# -----------------------
@app.route("/api/chat", methods
