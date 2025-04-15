@echo off
echo Setting up virtual environment...

:: Check if virtualenv is installed, if not install it
where virtualenv >nul 2>&1
if %errorlevel% neq 0 (
    echo virtualenv is not installed. Installing...
    python -m pip install virtualenv
)

:: Create a virtual environment named "venv"
python -m virtualenv venv

:: Activate the virtual environment
call venv\Scripts\activate.bat

echo Installing dependencies...

:: Install ALL required dependencies, including Flask and psutil
pip install Flask psutil opencv-python mediapipe websocket-client speech_recognition google-generativeai pyaudio gTTS playsound

echo Dependencies installed.
echo.
echo Virtual environment "venv" is now active.
echo To deactivate it, run "deactivate" in the command prompt.
pause