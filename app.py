# app.py (Updated with new voice and personality)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from google.cloud import texttospeech
import os
import base64

# Setup Flask
app = Flask(__name__)
CORS(app)

# --- IMPORTANT: MAKE SURE TO REPLACE THESE VALUES ---
# Configure Gemini API (replace with your API key)
genai.configure(api_key="AIzaSyDFV1gs4qVYnKtBRJO3jDp6rumNscYvbcI") 
model = genai.GenerativeModel("gemini-1.5-pro")

# Setup Google Cloud credentials (replace with your file path)
# After (Example for your computer)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/aryangarg/Desktop/GEN_AI/service-account.json"
# ----------------------------------------------------


# Setup Google Text-to-Speech
tts_client = texttospeech.TextToSpeechClient()

# --- ROUTES TO SERVE HTML PAGES ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/voice")
def voice_page():
    return render_template("voice.html")
# ----------------------------------------


@app.route("/api/chat", methods=["POST"])
def chat_api():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # --- CHANGE #1: NEW PERSONALITY PROMPT ---
        # This new, more detailed prompt instructs the AI to be brief, caring, and a better listener.
        prompt = f"""
        You are Mindwell, a caring AI companion. Your goal is to listen and provide gentle, supportive responses.
        A user has shared the following: '{user_message}'

        Your task:
        1. Keep your reply very short, ideally one or two caring sentences.
        2. Use a warm, empathetic, and non-judgmental tone.
        3. Do not give complex advice. Instead, validate their feelings and make them feel heard.
        4. If appropriate, you can ask a simple, open-ended question to show you are listening.

        Your gentle reply:
        """
        
        response = model.generate_content(prompt)
        reply_text = response.text

        # --- CHANGE #2: NEW HUMAN-LIKE VOICE ---
        # We are switching to a high-quality WaveNet voice for a more natural sound.
        synthesis_input = texttospeech.SynthesisInput(text=reply_text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-F",  # A calm, female WaveNet voice. You can also try "en-US-Wavenet-D" for a male voice.
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        tts_response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        audio_base64 = base64.b64encode(tts_response.audio_content).decode("utf-8")

        return jsonify({"reply": reply_text, "audio": audio_base64})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)