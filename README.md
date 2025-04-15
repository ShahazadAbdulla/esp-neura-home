# Home Automation Project

This project automates a home using **gesture recognition** (via OpenCV) and **voice commands** (via Gemini API). It allows you to control **LED lights**, **fan**, and **video playback** through hand gestures and voice commands, with an **ESP32** controlling the devices and a **web interface** displaying the status.

## Features
- **Gesture Control**: Control **LED lights**, **fan**, and **video playback** using hand gestures via **OpenCV**.
- **Voice Control**: Use voice commands (e.g., "Turn on the light") to control devices via the **Gemini API**.
- **Web Interface**: View and control device status (LED, Fan, Video) via a web page.
- **ESP32 Control**: **ESP32** microcontroller controls the devices and handles WebSocket communication.

## Project Structure
(Based on recent updates)
<pre>
Home Automation/
├── Main_code/
│   ├── server.py         # Flask web server application
│   ├── static/           # Static files for the web interface (CSS, JS, Images)
│   │   ├── arc-reactor.png
│   │   ├── demo.mp4
│   │   ├── fan.png
│   │   └── led.png
│   └── templates/        # HTML templates and related scripts
│       ├── index.html      # Main web interface page
│       ├── opencv.py       # OpenCV gesture recognition code
│       └── Speech.py       # Speech recognition code using Gemini API
├── install_dependencies.bat # Windows script to install Python packages in a venv
└── README.md             # This file
</pre>

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

## Installation

Follow these steps to set up the project on your system:

1.  **Run the `install_dependencies.bat` script:**
    *   Locate the `install_dependencies.bat` file in the project directory.
    *   Double-click `install_dependencies.bat` to run it.
    *   This script will:
        *   Create a virtual environment named `venv`.
        *   Activate the virtual environment.
        *   Install all the required Python packages listed in the script.
    *   **Important:** The script will open a command prompt window. Wait for the script to finish installing all the dependencies. You'll see a message "Dependencies installed."

2.  **Alternative: Manual Dependency Installation (If `install_dependencies.bat` fails or on non-Windows):**
    *   Open a command prompt (Windows) or terminal (macOS/Linux).
    *   Navigate to the project directory using the `cd` command.
    *   Create a virtual environment: `python -m venv venv`
    *   Activate the virtual environment:
        *   Windows: `venv\Scripts\activate`
        *   macOS/Linux: `source venv/bin/activate`
    *   Install the dependencies: `pip install Flask psutil opencv-python mediapipe websocket-client speech_recognition google-generativeai pyaudio gTTS playsound`

3.  **Install `pyaudio` (If manual installation fails):**
    *   If you encounter errors during the `pyaudio` installation (especially on Windows), try the following within the activated virtual environment:
        *   `pip install pipwin`
        *   `pipwin install pyaudio`

## Configuration

Before running the project, you'll need to configure the following:

1.  **Google Gemini API Key:**
    *   Edit the `Main code/templates/Speech.py` file.
    *   Find the line `genai.configure(api_key="YOUR_API_KEY")`.
    *   Replace `"YOUR_API_KEY"` with your actual Google Gemini API key.

2.  **ESP32 IP Address:**
    *   Edit the `Main code/templates/opencv.py` and `Main code/templates/Speech.py` files.
    *   Find the line `ESP32_IP = "ws://192.168.13.254:81"` (or similar).
    *   Replace the IP address and port with the correct WebSocket address of your ESP32 microcontroller. Ensure your ESP32 is running compatible firmware.

3.  **File Paths (Verify in `Main code/server.py`):**
    *   Edit the Flask app script: `Main code/server.py`.
    *   Locate the lines where `opencv.py` and `Speech.py` are launched (likely using `subprocess.Popen`).
    *   Ensure the paths used are relative and correct, pointing to the scripts within the `templates` folder (e.g., `"templates/opencv.py"` and `"templates/Speech.py"`).

## Running the Project

1.  **Activate the Virtual Environment (If not already active):**
    *   Open a command prompt (Windows) or terminal (macOS/Linux).
    *   Navigate to the project directory.
    *   Activate the virtual environment:
        *   Windows: `venv\Scripts\activate`
        *   macOS/Linux: `source venv/bin/activate`

2.  **Run the Flask App:**
    *   Execute the command from the project's root directory:
      ```bash
      python "Main code/server.py"
      ```
    *   This will start the Flask web server. Look for output indicating the server is running, usually on `http://127.0.0.1:5000/`.

3.  **Access the Web Interface:**
    *   Open a web browser and go to `http://127.0.0.1:5000/` or `http://localhost:5000/`.

4.  **Use the Web Interface:**
    *   Use the buttons on the web interface to start and stop the computer vision (`opencv.py`) and voice control (`Speech.py`) systems as separate processes.

## Troubleshooting

*   **Dependency Installation Errors:**
    *   Ensure you have Python 3.x and pip installed correctly.
    *   Try running the `install_dependencies.bat` script as an administrator (Windows: right-click -> Run as administrator).
    *   If `pyaudio` installation fails, follow the specific instructions in the Installation section.
*   **"ModuleNotFoundError" Errors:**
    *   Make sure you have activated the virtual environment (`venv\Scripts\activate` or `source venv/bin/activate`) *before* running the Python scripts (`python "Main code/server.py"`).
    *   Verify all dependencies were installed successfully. You can check with `pip list` inside the activated venv.
*   **Camera Access Issues:**
    *   Make sure your webcam is connected, enabled, and not being used by another application.
    *   Check your operating system's privacy settings to allow Python/terminal access to the camera.
*   **WebSocket Connection Errors:**
    *   Verify that your ESP32 is powered on, connected to the same network, and running the correct WebSocket server firmware.
    *   Double-check the ESP32 IP address configured in `Main code/templates/opencv.py` and `Main code/templates/Speech.py`.
    *   Check firewall settings on your computer that might block outgoing WebSocket connections.
*   **Gemini API Errors:**
    *   Ensure that you have a valid Google Gemini API key.
    *   Verify that you have correctly configured the API key in `Main code/templates/Speech.py`.
    *   Check your Gemini API usage limits and billing status.
*   **"Port already in use" Error (e.g., Port 5000):**
    *   This means another application is using that network port. Stop the other application or change the port the Flask app uses. Edit `Main code/server.py`, find the `app.run(...)` line, and change the `port` argument (e.g., `app.run(host='0.0.0.0', port=5001, debug=True)`). Remember to access the web interface using the new port (`http://127.0.0.1:5001/`).

## How It Works
- **Web Server (`server.py`)**: A Flask application that serves the HTML interface (`templates/index.html`) and static files (`static/`). It provides API endpoints or buttons that use `subprocess` to launch the `opencv.py` and `Speech.py` scripts as separate processes.
- **Gesture Control (`templates/opencv.py`)**: Uses OpenCV and MediaPipe to detect hand gestures via the camera. When a recognized gesture corresponding to a command is detected, it sends a message (e.g., "LED ON") via WebSocket to the configured ESP32 IP address.
- **Voice Control (`templates/Speech.py`)**: Uses SpeechRecognition and PyAudio to capture audio from the microphone. The captured audio is sent to the Google Gemini API for transcription and potentially command interpretation. Recognized commands are sent via WebSocket to the ESP32.
- **ESP32**: (Requires separate firmware) Listens for incoming WebSocket messages. When a command like "LED ON" is received, it controls the corresponding hardware (e.g., toggles a GPIO pin connected to an LED). It might also send status updates back via WebSocket, although this is not detailed here.

## Teammates:
- Shahazad Abdulla
- Sidharth Sajith
- Tharun Oommmen Jacob

