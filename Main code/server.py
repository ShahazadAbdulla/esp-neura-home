from flask import Flask, render_template, jsonify
import os
import subprocess
import signal  # For process termination
import psutil # For process existence check
import time # For adding a small delay
import threading # Import threading

app = Flask(__name__)

# --- Global variable to store the OpenCV process ID ---
opencv_process = None
speech_process = None # Global variable for speech process

@app.route("/")
def index():
    return render_template('index.html') # Assuming your HTML file is named 'index.html'

@app.route("/launch_opencv", methods=['POST'])
def launch_opencv():
    global opencv_process
    if opencv_process is None or not psutil.pid_exists(opencv_process.pid): # More robust check if process is running
        try:
            opencv_script_path = "C:\\Users\\LENOVO\\Desktop\\Coding\\projects\\NeuraHome\\AI home automation UI\\templates\\openCV.py" # **<-- IMPORTANT: Set your correct path here!**
            # Use subprocess.Popen to launch in a new terminal window (platform-dependent)
            # For Windows (cmd):
            opencv_process = subprocess.Popen(['start', 'cmd', '/k', 'python', opencv_script_path], shell=True)
            # For Linux (xterm):
            # opencv_process = subprocess.Popen(['xterm', '-e', 'python', opencv_script_path])
            # For macOS (Terminal.app using open):
            # opencv_process = subprocess.Popen(['open', '-a', 'Terminal', 'python', opencv_script_path])

            print(f"[Server] Launched OpenCV script with PID: {opencv_process.pid}")
            return jsonify({'status': 'success', 'message': f'OpenCV script launched with PID: {opencv_process.pid}'}) # Include PID in success message
        except Exception as e:
            print(f"[Server] Error launching OpenCV script: {e}")
            return jsonify({'status': 'error', 'message': f'Error launching script: {e}'}), 500
    else:
        return jsonify({'status': 'warning', 'message': 'OpenCV script is already running.'})

@app.route("/terminate_opencv", methods=['POST'])
def terminate_opencv():
    global opencv_process
    if opencv_process and psutil.pid_exists(opencv_process.pid): # More robust check if process is running
        pid = opencv_process.pid
        print(f"[Server] Attempting FORCEFUL termination of OpenCV script with PID: {pid}") # Log forceful termination attempt
        try:
            if os.name == 'nt': # Windows - FORCEFUL TERMINATION
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)

                print(f"[Server] Terminating {len(children)} child processes...") # Log number of child processes
                for child in children:
                    print(f"[Server] Terminating child process: {child.pid}")
                    child.terminate() # Try terminate first
                gone_children, alive_children = psutil.wait_children(parent, timeout=3) # Wait a short time for children
                if alive_children:
                    print(f"[Server] Forcefully killing {len(alive_children)} child processes...") # Log forceful kill for remaining children
                    for child in alive_children:
                        print(f"[Server] Forcefully killing child process: {child.pid}")
                        child.kill() # Forcefully kill remaining children

                print(f"[Server] Terminating parent process: {pid}")
                parent.terminate() # Try terminate parent
                gone_parent, alive_parent = psutil.wait_children(parent, timeout=5) # Wait for parent
                if alive_parent:
                    print(f"[Server] Forcefully killing parent process: {parent.pid}") # Log forceful kill for parent if needed
                    parent.kill() # Forcefully kill parent if still alive


            else: # Linux/macOS - FORCEFUL TERMINATION (using SIGKILL directly)
                print(f"[Server] Forcefully killing process PID: {pid} using SIGKILL") # Log SIGKILL usage
                os.kill(pid, signal.SIGKILL) # Forcefully kill using SIGKILL

            opencv_process = None # Reset the process variable
            print(f"[Server] FORCEFUL termination attempted for OpenCV script (PID: {pid}).") # Indicate forceful attempt
            return jsonify({'status': 'success', 'message': f'FORCEFUL termination attempted for OpenCV script (PID: {pid}).'}) # Updated message
        except Exception as e:
            print(f"[Server] Error during FORCEFUL termination of OpenCV script (PID: {pid}): {e}") # Log errors during forceful termination
            return jsonify({'status': 'error', 'message': f'Error during forceful termination (PID: {pid}): {e}'}), 500
    else:
        return jsonify({'status': 'warning', 'message': 'OpenCV script is not running or already terminated.'})

def start_speech_recognition(): # Function to start speech.py
    global speech_process
    if speech_process is None or not psutil.pid_exists(speech_process.pid):
        try:
            speech_script_path = "C:\\Users\\LENOVO\\Desktop\\Coding\\projects\\NeuraHome\\AI home automation UI\\templates\\speech.py" # **<-- IMPORTANT: Set your correct path here!**
            # Launch speech.py in a new terminal (similar to opencv.py)
            speech_process = subprocess.Popen(['start', 'cmd', '/k', 'python', speech_script_path], shell=True)
            print(f"[Server] Launched speech.py with PID: {speech_process.pid}")
        except Exception as e:
            print(f"[Server] Error launching speech.py: {e}")

@app.route("/start_voice_control", methods=['POST']) # New endpoint to trigger voice from frontend
def start_voice_control():
    start_speech_recognition() # Just call the function to start speech.py
    return jsonify({'status': 'success', 'message': 'Voice control started (if not already running).'})

@app.route("/stop_voice_control", methods=['POST']) # Optional endpoint to stop voice control
def stop_voice_control():
    global speech_process
    if speech_process and psutil.pid_exists(speech_process.pid):
        pid = speech_process.pid
        print(f"[Server] Attempting to terminate speech.py with PID: {pid}")
        try:
            if os.name == 'nt': # Windows - similar forceful termination as opencv
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.terminate()
                parent.terminate()
            else: # Linux/macOS - SIGKILL
                os.kill(pid, signal.SIGKILL)
            speech_process = None
            return jsonify({'status': 'success', 'message': f'Speech control terminated (PID: {pid}).'})
        except Exception as e:
            print(f"[Server] Error terminating speech.py: {e}")
            return jsonify({'status': 'error', 'message': f'Error terminating speech control: {e}'}), 500
    else:
        return jsonify({'status': 'warning', 'message': 'Speech control is not running.'})


if __name__ == '__main__':
    threading.Thread(target=start_speech_recognition).start() # Start speech recognition when Flask server starts
    app.run(debug=True, host='0.0.0.0', port=5000) # Run Flask server locally