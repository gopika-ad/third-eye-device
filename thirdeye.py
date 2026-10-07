import cv2
import requests
import numpy as np
import time
import speech_recognition as sr
from PIL import Image
import google.generativeai as genai
from gtts import gTTS
import pygame
import tempfile
import os

# ── Config ────────────────────────────────────────
API_KEY   = "AIzaSyDRyg0rVJdrNfOoOtvFwoGKd00H-PeNDfM"
ESP32_URL = "http://10.211.121.142/capture"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-live-preview')

is_speaking = False

# ── Wake word variations ───────────────────────────
WAKE_WORDS = [
    "third eye", "thirdeye", "thirdye", "third i",
    "that i", "third eyes", "thirty eye", "third a",
    "third", "thirdi", "turdeye", "therd eye"
]

# ── Speech ────────────────────────────────────────
def speak(text):
    global is_speaking
    is_speaking = True
    print(f"ThirdEye: {text}")
    try:
        tts = gTTS(text=text.replace("*", ""), lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
        tts.save(tmp_path)
        pygame.mixer.init()
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        os.remove(tmp_path)
    except Exception as e:
        print(f"Speech error: {e}")
    is_speaking = False

# ── Check if wake word is in spoken text ──────────
def contains_wake_word(text):
    text = text.lower().strip()
    for w in WAKE_WORDS:
        if w in text:
            return True
    return False

# ── Extract command after wake word ───────────────
def extract_command(text):
    text = text.lower().strip()
    for w in WAKE_WORDS:
        if w in text:
            after = text.split(w, 1)[-1].strip()
            return after
    return text

# ── AI analysis ───────────────────────────────────
def analyze(command):
    speak("Analyzing.")
    try:
        response = requests.get(ESP32_URL, timeout=25)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is not None:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img   = Image.fromarray(rgb_frame)

                if command:
                    prompt = f"You are assisting a visually impaired person. They asked: '{command}'. Answer based only on what you see in this image. Be concise and clear."
                else:
                    prompt = "Describe this scene for a visually impaired person. Focus on obstacles, people, text, and layout. Be concise."

                ai_response = model.generate_content([prompt, pil_img])
                print(f"AI Response: {ai_response.text}")
                speak(ai_response.text)
            else:
                speak("Error decoding image.")
        else:
            speak("Could not reach the camera.")

    except Exception as e:
        speak("Analysis failed.")
        print(e)

# ── Main listening loop ────────────────────────────
def listen_loop():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8

    print("Listening for wake word: 'Third Eye'")

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Ready. Say 'Third Eye' followed by your question.")

        while True:
            if is_speaking:
                time.sleep(0.2)
                continue

            try:
                print("Waiting for speech...")
                audio = r.listen(source, timeout=10, phrase_time_limit=8)
                text = r.recognize_google(audio).lower()
                print(f"Heard: {text}")

                if contains_wake_word(text):
                    command = extract_command(text)
                    print(f"Wake word detected! Command: '{command}'")
                    analyze(command)
                else:
                    print("No wake word, ignoring.")

            except sr.WaitTimeoutError:
                print("Still listening...")
            except sr.UnknownValueError:
                print("Couldn't understand, still listening...")
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

# ── Main ──────────────────────────────────────────
if __name__ == "__main__":
    speak("Third Eye online. Say Third Eye followed by your question.")
    listen_loop()