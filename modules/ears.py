# modules/ears.py
import pyaudiowpatch as pyaudio
import sys
import speech_recognition as sr

# The 2026 Mic Fix for Python 3.14
sys.modules['pyaudio'] = pyaudio

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except Exception:
            return "none"