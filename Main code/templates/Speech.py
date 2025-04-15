import speech_recognition as sr
import websocket
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import threading
import time
import signal
import sys

# ESP32 WebSocket IP (replace with your actual ESP32 IP)
ESP32_IP = "ws://192.168.13.254:81"  # Replace with your ESP32 IP address

# Gemini API Key (replace with your actual key)
genai.configure(api_key="AIzaSyAx9VLRb83uZk0pjCq7p_O54ryaCLl2QNo")

# API limit variables
MAX_REQUESTS_PER_MINUTE = 15
request_counter = 0
last_request_time = time.time()

# Valid commands in uppercase
VALID_COMMANDS = ["LED ON", "LED OFF", "FAN ON", "FAN OFF", "VIDEO PLAY", "VIDEO PAUSE"]

def fallback_map_command(command):
    """Local keyword-based mapping for simple commands using expanded synonyms."""
    cmd = command.lower()
    # Synonyms for lights
    light_keywords = ["light", "lights", "lamp", "led", "illumination", "illuminate", "bright"]
    light_on_synonyms = [
        "on", "start", "activate", "turn on", "switch on", "brighten", "enable", 
        "light it up", "ignite", "illumine"
    ]
    light_off_synonyms = [
        "off", "stop", "deactivate", "dim", "disable", "turn off", "switch off", 
        "extinguish", "shut off", "kill", "darken", "unlight"
    ]
    
    # Synonyms for fan
    fan_keywords = ["fan", "breeze"]
    fan_on_synonyms = [
        "on", "start", "activate", "turn on", "switch on", "run"
    ]
    fan_off_synonyms = [
        "off", "stop", "deactivate", "turn off", "switch off", "kill"
    ]
    
    # Synonyms for video
    video_keywords = ["video", "movie", "film", "clip", "stream", "playback"]
    video_play_synonyms = [
        "play", "start", "activate", "begin", "launch", "run", "open"
    ]
    video_pause_synonyms = [
        "pause", "stop", "halt", "freeze", "hold", "interrupt", "suspend"
    ]
    
    # Check for light commands.
    if any(word in cmd for word in light_keywords):
        if any(phrase in cmd for phrase in light_off_synonyms):
            return "LED OFF"
        elif any(phrase in cmd for phrase in light_on_synonyms):
            return "LED ON"
    
    # Check for fan commands.
    if any(word in cmd for word in fan_keywords):
        if any(phrase in cmd for phrase in fan_off_synonyms):
            return "FAN OFF"
        elif any(phrase in cmd for phrase in fan_on_synonyms):
            return "FAN ON"
    
    # Check for video commands.
    if any(word in cmd for word in video_keywords):
        if any(phrase in cmd for phrase in video_pause_synonyms):
            return "VIDEO PAUSE"
        elif any(phrase in cmd for phrase in video_play_synonyms):
            return "VIDEO PLAY"
    
    return "UNKNOWN"

def get_intent(command):
    """Determine command intent using local mapping with fallback to Gemini API."""
    global request_counter, last_request_time

    # First, try local mapping.
    local_intent = fallback_map_command(command)
    if local_intent != "UNKNOWN":
        print(f"(Local mapping used: {local_intent})")
        return local_intent

    # Throttling based on API limits.
    if request_counter >= MAX_REQUESTS_PER_MINUTE:
        time_elapsed = time.time() - last_request_time
        if time_elapsed < 60:
            print(f"API limit reached. Sleeping for {60 - time_elapsed:.1f} seconds...")
            time.sleep(60 - time_elapsed)
        request_counter = 0
        last_request_time = time.time()

    prompt = (
        "Analyze this command and return ONLY one of the following actions EXACTLY as shown (in UPPERCASE): "
        "LED ON, LED OFF, FAN ON, FAN OFF, VIDEO PLAY, VIDEO PAUSE. "
        f"Command: {command}"
    )

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    try:
        response = model.generate_content(prompt)
        request_counter += 1
        action = response.text.strip().upper()
        print(f"(Gemini response: {action})")
        for cmd in VALID_COMMANDS:
            if cmd in action:
                return cmd
        return "UNKNOWN"
    except ResourceExhausted as e:
        print(f"Error: {e}. Retrying in 30 seconds...")
        time.sleep(30)
        return "UNKNOWN"

def on_message(ws, message):
    """Handles incoming messages from the ESP32."""
    print(f"Received from ESP32: {message}")

def on_error(ws, error):
    """Handles WebSocket errors."""
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handles WebSocket closure."""
    print("WebSocket closed")

def on_open(ws):
    """Handles WebSocket connection open."""
    print("WebSocket connected")

def execute_command(action, ws):
    """Send the resolved command to ESP32."""
    if action in VALID_COMMANDS:
        print(f"Sending: {action}")
        ws.send(action)
    else:
        print("⚠️ Unknown command")

def listen_and_process():
    recognizer = sr.Recognizer()
    
    # Establish WebSocket connection.
    ws = websocket.WebSocketApp(
        ESP32_IP,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    # Set the WebSocket thread as a daemon so it won't block process exit.
    websocket_thread = threading.Thread(target=ws.run_forever)
    websocket_thread.daemon = True
    websocket_thread.start()

    with sr.Microphone() as source:
        print("🎤 Listening for commands... (Press Ctrl+C to stop)")
        while True:
            try:
                print("🔄 Ready... Speak now!")
                audio = recognizer.listen(source, phrase_time_limit=5)
                recognized_text = recognizer.recognize_google(audio)
                print(f"🎙 Recognized: {recognized_text}")

                action = get_intent(recognized_text)
                execute_command(action, ws)

            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError:
                print("⚠️ Speech recognition service unavailable")
            except sr.WaitTimeoutError:
                print("⌛ No speech detected. Waiting for input...")
                continue
            except KeyboardInterrupt:
                print("\n🛑 Stopping voice control via Ctrl+C...")
                ws.close()
                sys.exit(0)

def stop_program(signal, frame):
    """Gracefully exit the program when Ctrl+C is pressed."""
    print("\n🛑 Exiting program...")
    sys.exit(0)

if __name__ == "__main__":
    # Optionally register the SIGINT handler.
    signal.signal(signal.SIGINT, stop_program)
    listen_and_process()
