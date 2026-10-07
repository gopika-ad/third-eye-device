# Third Eye Device: AI-Powered Smart Glasses for the Visually Impaired

An assistive smart glasses system designed to help visually impaired individuals navigate their surroundings independently through real-time scene analysis, obstacle detection, and voice feedback.

## Key Features
- **Real-Time Scene Capture:** Integrates with an ESP32-CAM to stream live visual input.
- **AI Scene Description:** Analyzes captured frames to identify objects, text, and environmental context.
- **Voice Commands:** The system is activated with the wake word **"Third Eye"** followed by a question.
- **Audio Feedback:** Converts scene descriptions into clear speech output (`response.mp3`) for the user.
- **Obstacle Alert:** Uses an ultrasonic sensor to detect nearby obstacles and sounds a buzzer when an object is within the set distance.
- **Wi-Fi Communication:** Transfers captured images from the ESP32-CAM to the processing system.

## Tech Stack
- **Languages:** Python, C++ (ESP32 firmware)
- **Libraries & APIs:** OpenCV, Requests, gTTS
- **AI:** Google Gemini API (`google.genai`)
- **Hardware:** ESP32-CAM, HC-SR04 ultrasonic sensor, buzzer

## How It Works
1. The user says the wake word **"Third Eye"** followed by a question.
2. The ESP32-CAM captures the scene and sends the frame over Wi-Fi.
3. The frame and question are sent to the Gemini model, which returns a short, useful description.
4. The response is converted to speech and played back to the user.
5. In parallel, the ultrasonic sensor monitors distance and sounds the buzzer when an obstacle is too close.

## Getting Started

### Prerequisites
- Python 3.9 or newer
- An ESP32-CAM flashed with the project firmware
- A Gemini API key

### Installation
```bash
git clone https://github.com/gopika-ad/third-eye-device.git
cd third-eye-device
pip install opencv-python requests gTTS google-genai
```

### Configuration
Set your API key before running:

```bash
# Linux / macOS
export GEMINI_API_KEY="your-api-key"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key"
```

Then update the ESP32-CAM IP address in `thirdeye.py` to match your network.

### Run
```bash
python thirdeye.py
```

To check that your camera connection works first, run `python test_cam.py`.

## Project Structure
```
├── thirdeye.py        # Main script: capture, AI query, speech output
├── bot.py             # Audio listener and command handling
├── test_cam.py        # ESP32-CAM stream connection test utility
├── firmware/          # ESP32-CAM firmware
├── response.mp3       # Generated speech output
└── README.md          # Project documentation
```

## Acknowledgements
Developed as a B.Tech minor project at Viswajyothi College of Engineering and Technology (VJCET), under APJ Abdul Kalam Technological University.
