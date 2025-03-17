from gtts import gTTS
import os

def generate_tts(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    file_path = "static/output.mp3"
    tts.save(file_path)
    return file_path
