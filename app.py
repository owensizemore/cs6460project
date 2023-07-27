import os

import openai
import io
import google.cloud.texttospeech as tts
from flask import Flask, redirect, render_template, jsonify, request, url_for, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key"
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "cs6460-project-391710-dcae76e5282f.json"

astica_key = os.getenv("ASTICA_KEY")
prompts_and_responses = []
accents = []

@app.route("/", methods=("GET", "POST"))
def index():
    global prompts_and_responses
    global accents
    
    if request.method == "POST":
        # Add user's specified langauge
        if "language" in request.form:
            language = request.form["language"]
            session["language"] = language

        # Add user's specified language level
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

        # Delete all session variables and start fresh
        elif "new_session" in request.form:
            if "language" in session:
                session.pop("language")
            if "level" in session:
                session.pop("level")
            if "initial_prompt" in session:
                session.pop("initial_prompt")
            prompts_and_responses = []
            accents = []

        # Gather input from user (text only right now)
        elif "user_input" in request.form:
            input = request.form.get("user_text_input")
            prompt = create_user_response_prompt(
                language=session["language"],
                level=session["level"],
                user_response=input
            )
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.6,
                max_tokens=1024
            ).choices[0].text
            prompts_and_responses.append((input, response))

    # Retrieve existing session variables if they were not created anew
    language = session.get("language")
    level = session.get("level")
    initial_prompt = session.get("initial_prompt")

    # Get language accents (if applicable)
    accents = get_language_accents(language)

    # Render template with all variables
    return render_template(
        "index.html", 
        language=language,
        level=level,
        initial_prompt=initial_prompt,
        prompts_and_responses=prompts_and_responses,
        accents=accents
    )

@app.route('/process-text', methods=["POST"])
def process_text():
    text = request.form.get("text")
    prompt = create_user_response_prompt(
        language=session["language"],
        level=session["level"],
        user_response=text
    )
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=1024
    ).choices[0].text
    prompts_and_responses.append((text, response))

    # Retrieve existing session variables if they were not created anew
    language = session.get("language")
    level = session.get("level")
    initial_prompt = session.get("initial_prompt")

    # Render template with all variables
    return render_template(
        "index.html", 
        language=language,
        level=level,
        initial_prompt=initial_prompt,
        prompts_and_responses=prompts_and_responses,
        accents=accents
    )

@app.route('/process-audio', methods=["POST"])
def process_audio():
    try:
        audio_file = request.files["audio"]

        # Get the original filename and file extension
        original_filename = audio_file.filename
        file_extension = os.path.splitext(original_filename)[1]
        
        # Save the uploaded audio file locally with the original filename and extension
        save_filename = "uploaded_audio" + file_extension
        audio_file.save(save_filename)

        # Perform audio transcription using OpenAI's Whisper library
        with open(save_filename, "rb") as audio_file:
            user_audio_prompt = openai.Audio.transcribe("whisper-1", audio_file)

        prompt_transcription = user_audio_prompt['text']

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_transcription,
            temperature=0.6,
            max_tokens=1024
        ).choices[0].text
        prompts_and_responses.append((prompt_transcription, response))

        # Retrieve existing session variables if they were not created anew
        language = session.get("language")
        level = session.get("level")
        initial_prompt = session.get("initial_prompt")

        # Render template with all variables
        return render_template(
            "index.html", 
            language=language,
            level=level,
            initial_prompt=initial_prompt,
            prompts_and_responses=prompts_and_responses,
            accents=accents
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dictate', methods=["POST"])
def dictate():
    text = request.form.get("text")
    audio_file = generate_audio(text)
    return jsonify({'audio_url': audio_file})

@app.route('/process_image', methods=["POST"])
def process_image():
    global prompts_and_responses

    image_file = request.files['image']
    # image_file.save("uploaded_image.jpg")

    prompts_and_responses.append((image_file, "That's a cool image!")) # TODO currently unable to display actual image in HTML

    # Rerendering
    return render_template(
        "index.html", 
        language=session.get("language"),
        level=session.get("level"),
        initial_prompt=session.get("initial_prompt"),
        prompts_and_responses=prompts_and_responses
    )

def generate_audio(text):
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code=get_language_code(session["language"]),
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

def get_language_code(language):
    codes = {
        'english': 'en-US',
        'spanish': 'es-US',
        'french': 'fr-FR',
        'portuguese': 'pt-BR',
        'german': 'de-DE',
        'afrikaans': 'af-ZA',
        'arabic': 'ar-XA',
        'filipino': 'fil-PH',
        'italian': 'it-IT',
        'japanese': 'ja-JP',
        'chinese': 'zh-CN',
        'vietnamese': 'vi-VN',
        'korean': 'ko-KR'
    }
    language = language.lower()
    return codes[language]

def get_language_accents(language):
    accent_mapping = {
        "spanish": ['á', 'é', 'í', 'ñ', 'ó'],
        "french": ['à', 'â', 'é', 'è', 'ê', 'î', 'ô', 'ù', 'û'],
        "portuguese": ['á', 'â', 'ã', 'à', 'é', 'ê', 'í', 'ó', 'ô', 'õ', 'ú']
    }
    if language is not None:
        language = language.lower()
        return accent_mapping.get(language, [])
    return []

def create_initial_prompt(language, level):
    return f"""Pretend that you are a foreign language tutor that is fluent in {language}. 
    Your job is to maintain a conversation with a student that is capable of communicating in {language} at the level of {level}.
    Whenever the student responds to you, you must give a relevant reply. Respond to this prompt with a generic greeting message 
    introducing yourself as the student's tutor, ensuring that your greeting is appropriate for students at the level of {level}."""

def create_user_response_prompt(language, level, user_response):
    return f"""Pretend that you are a foreign language tutor that is fluent in {language}.
    A student, who is capable of communicating in {language} at the level of {level}, has just said this to you:
    
    {user_response}
    
    Construct an appropriate response to this message at the level of {level} that will keep the conversation going, asking follow-up questions as necessary."""
