# assistant.py
from llm import build_llm
from stt import speech_to_text
from tts import speak
import re

class VoiceAssistant:
    def __init__(self):
        self.conversation = build_llm()

    def run(self):
        print("💻 CodeMate (Voice Coding Assistant) is running. Press Enter to talk. Say 'exit' to quit.")
        while True:
            input("Press Enter to record...")
            text = speech_to_text()
            if not text:
                continue

            print(f"🗣️ You said: {text}")

            if text.lower() in ["exit", "quit", "stop"]:
                print("👋 Goodbye!")
                break

            reply = self.conversation.predict(input=text)
            
            # Check if response contains code (triple backticks)
            has_code = bool(re.search(r'```.*?```', reply, re.DOTALL))
            
            print(f"🤖 CodeMate: {reply}")
            
            if has_code:
                # Speak only a brief summary if code is present
                summary = "Here's the code you requested. Please check the printed output for details."
                speak(summary)
            else:
                # Speak full response if no code
                speak(reply)