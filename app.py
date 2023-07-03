import os

import openai
import google.cloud.texttospeech as tts
from flask import Flask, redirect, render_template, jsonify, request, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "cs6460-project-391710-dcae76e5282f.json"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        if "language" in request.form:
            language = request.form["language"]
            session["language"] = language

        elif "level" in request.form:
            level = request.form["level"]
            session["level"] = level

            # Send initial prompt to OpenAI API if one doesn't exist already
            if "initial_prompt" not in session:
                prompt = create_initial_prompt(session["language"], session["level"])
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0.6,
                    max_tokens=1024
                )
                session["initial_prompt"] = response.choices[0].text

        elif "user_response" in request.form:
            user_response = request.form["user_response"]
            prompt = create_user_response_prompt(
                language=session["language"],
                level=session["level"],
                user_response=user_response
            )
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.6,
                max_tokens=1024
            )
            session["user_response"] = user_response
            session["prompt_reply"] = response.choices[0].text

        elif "new_session" in request.form:
            if "language" in session:
                session.pop("language")
            if "level" in session:
                session.pop("level")
            if "initial_prompt" in session:
                session.pop("initial_prompt")
            if "user_response" in session:
                session.pop("user_response")
            if "prompt_reply" in session:
                session.pop("prompt_reply")

    language = session.get("language")
    level = session.get("level")
    initial_prompt = session.get("initial_prompt")
    user_response = session.get("user_response")
    prompt_reply = session.get("prompt_reply")

    return render_template(
        "index.html", 
        language=language,
        level=level,
        initial_prompt=initial_prompt,
        user_response=user_response,
        prompt_reply=prompt_reply
    )

@app.route('/dictate', methods=["POST"])
def dictate():
    text = request.form.get("text")
    audio_file = generate_audio(text)
    return jsonify({'audio_url': audio_file})

def generate_audio(text):
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code='es-US',
        ssml_gender=tts.SsmlVoiceGender.FEMALE
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    audio_file_path = 'static/audio_output.mp3'

    with open(audio_file_path, 'wb') as out_file:
        out_file.write(response.audio_content)

    return audio_file_path

def create_initial_prompt(language, level):
    return f"""Pretend that you are a foreign language tutor that is fluent in {language}. 
    Your job is to maintain a conversation with a student that is capable of communicating in {language} at the level of {level}.
    Whenever the student responds to you, you must give a relevant reply. Respond to this prompt with a generic greeting message 
    introducing yourself as the student's tutor, ensuring that your greeting is appropriate for students at the level of {level}."""

def create_user_response_prompt(language, level, user_response):
    return f"""Pretend that you are a foreign language tutor that is fluent in {language}.
    A student, who is capable of communicating in {language} at the level of {level}, has just said this to you:
    
    {user_response}
    
    Construct an appropriate response to this message at the level of {level}."""
