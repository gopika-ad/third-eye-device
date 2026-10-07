import cv2
import pyttsx3
import speech_recognition as sr
from ultralytics import YOLO
import pytesseract
import face_recognition
import numpy as np
import time

# -----------------------------
# Voice Engine
# -----------------------------
engine = pyttsx3.init()
engine.setProperty('rate',150)

def speak(text):
    print("BOT:",text)
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# Speech Recognition
# -----------------------------
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("USER:",command)
        return command.lower()
    except:
        return ""

# -----------------------------
# Load Object Detection Model
# -----------------------------
model = YOLO("yolov8n.pt")

# ESP32 camera stream
url = "http://10.134.54.142"
cap = cv2.VideoCapture(url)

# -----------------------------
# Face Database
# -----------------------------
known_face_encodings = []
known_face_names = []

# Example: load known faces
# (add images of family members)

# -----------------------------
# Currency Labels (example)
# -----------------------------
currency_list = ["rupee","currency","note"]

# -----------------------------
# Chatbot Loop
# -----------------------------
speak("Third Eye assistant activated")

while True:

    command = listen()

    # -----------------------------
    # Object Detection
    # -----------------------------
    if "object" in command or "front" in command:

        ret, frame = cap.read()

        results = model(frame)

        for r in results:
            boxes = r.boxes

            for box in boxes:

                cls = int(box.cls[0])
                label = model.names[cls]

                speak(label)
                break

    # -----------------------------
    # Text Reading
    # -----------------------------
    elif "read" in command or "text" in command:

        ret, frame = cap.read()

        text = pytesseract.image_to_string(frame)

        if text.strip() != "":
            speak(text)
        else:
            speak("No text detected")

    # -----------------------------
    # Face Recognition
    # -----------------------------
    elif "who" in command or "person" in command:

        ret, frame = cap.read()

        rgb = frame[:,:,::-1]

        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        if len(face_encodings)==0:
            speak("No face detected")
        else:
            speak("Person detected")

    # -----------------------------
    # Currency Detection
    # -----------------------------
    elif "currency" in command or "money" in command:

        ret, frame = cap.read()

        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if label in currency_list:
                    speak("Currency detected")

    # -----------------------------
    # Navigation Assistance
    # -----------------------------
    elif "guide me" in command:

        speak("Scanning surroundings")

        ret, frame = cap.read()

        results = model(frame)

        obstacles = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                obstacles.append(model.names[cls])

        if len(obstacles)==0:
            speak("Path is clear")
        else:
            speak("Obstacle ahead")

    # -----------------------------
    # Emergency Feature
    # -----------------------------
    elif "help" in command:

        speak("Emergency mode activated")

    # -----------------------------
    # Exit
    # -----------------------------
    elif "stop" in command or "exit" in command:

        speak("Shutting down assistant")
        break