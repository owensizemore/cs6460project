import openai

openai.api_key_path = "apikey"

audio_file=open("testrecording.m4a", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript)