# Home Automation Project

This project automates a home using **gesture recognition** (via OpenCV) and **voice commands** (via Gemini API). It allows you to control **LED lights**, **fan**, and **video playback** through hand gestures and voice commands, with an **ESP32** controlling the devices and a **web interface** displaying the status.

## Features
- **Gesture Control**: Control **LED lights**, **fan**, and **video playback** using hand gestures via **OpenCV**.
- **Voice Control**: Use voice commands (e.g., "Turn on the light") to control devices via the **Gemini API**.
- **Web Interface**: View and control device status (LED, Fan, Video) via a web page.
- **ESP32 Control**: **ESP32** microcontroller controls the devices and handles WebSocket communication.

## Project Structure
<pre> 
  Home Automation/ 
  ├── Main_code/ # Main Arduino code for ESP32 
  │ └── website/ # Web interface for control and status display 
  ├── CVandVoice/ # Code for gesture and voice control 
  └── WS_test/ 
  ├── esp32/ # WebSocket test code for ESP32 
  └── Python/ # WebSocket test code for Python  </pre>


## Requirements
### **Hardware**
- **ESP32**: For controlling the **LED**, **fan**, and **video playback**.
- **Microphone**: For voice recognition using **Gemini API**.
- **Camera**: For gesture recognition using **OpenCV** and **MediaPipe**.

### **Software**
- **Arduino IDE**: To program the ESP32.
- **Python 3.x**: To run the gesture and voice control scripts.
- **Libraries**:
  - OpenCV: `pip install opencv-python`
  - MediaPipe: `pip install mediapipe`
  - SpeechRecognition: `pip install SpeechRecognition`
  - google-generativeai: `pip install google-generativeai`
  - websocket-client: `pip install websocket-client`
  - requests: `pip install requests`
  - pyaudio: `pip install pyaudio`

## Setup Instructions
1. **ESP32 Setup**:
   - Open **Arduino IDE** and install **ESP32 board**.
   - Open `Main_code/Main_code.ino` and upload to your **ESP32**.
   - Ensure **ESP32** is connected to the same Wi-Fi as your computer.

2. **Python Setup**:
   - Install Python libraries using:
     ```bash
     pip install opencv-python mediapipe SpeechRecognition google-generativeai websocket-client requests pyaudio
     ```
   - Set your **Gemini API key** in the **Speech.py** file.
   - Run **Speech.py** to enable voice control:
     ```bash
     python Speech.py
     ```
   - For **gesture control**, run the OpenCV code (`openCV.py`).

3. **Web Interface**:
   - Open `website/web.html` in a browser to control and view the status of devices (LED, Fan, Video).

## How It Works
- **Gesture Control**: The `openCV.py` script uses the camera to detect hand gestures and sends control commands (e.g., "LED ON") to the **ESP32**.
- **Voice Control**: The `Speech.py` script uses a microphone to listen for voice commands (e.g., "Turn on the light") and sends the command to **ESP32**.
- **ESP32**: The **ESP32** listens for WebSocket messages, processes the commands, and broadcasts the updated status (LED, Fan, Video) to the web interface.
## Teammates
- Shahazad Abdulla
- Sidharth Sajith
- Tharun Oommmen Jacob


