# tts.py
import pyttsx3

engine = pyttsx3.init()

def speak(text: str):
    print("🔊 Speaking...")
    engine.say(text)
    engine.runAndWait()
