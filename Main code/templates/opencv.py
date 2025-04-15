import cv2
import mediapipe as mp
import time
import math
import websocket

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
)
mp_draw = mp.solutions.drawing_utils

# Track FPS
prev_time = 0

# WebSocket setup to ESP32
ESP32_IP = "ws://192.168.13.254:81"  # Replace with your ESP32 IP address
ws = websocket.WebSocket()
ws.connect(ESP32_IP)

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return abs(ang)

# Function to draw additional lines for better visualization
def draw_extra_lines(frame, landmarks):
    h, w, _ = frame.shape
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    # Draw lines from wrist to all finger bases
    for i in [2, 5, 9, 13, 17]:  # Including thumb base
        cv2.line(frame, points[0], points[i], (255, 0, 0), 2)

    # Draw line between thumb base and index base
    cv2.line(frame, points[2], points[5], (0, 255, 255), 2)

# Gesture detection function using angles and distances
def detect_gesture(landmarks):
    h, w, _ = frame.shape
    points = [(lm.x * w, lm.y * h) for lm in landmarks]

    thumb_tip = points[4]
    thumb_base = points[2]
    index_tip = points[8]
    index_base = points[5]
    middle_tip = points[12]
    middle_base = points[9]
    ring_tip = points[16]
    ring_base = points[13]
    pinky_tip = points[20]
    pinky_base = points[17]
    wrist = points[0]

    # Check if fingers are extended (used for "Open Palm" and "Closed Fist")
    fingers_extended = [
        index_tip[1] < index_base[1],
        middle_tip[1] < middle_base[1],
        ring_tip[1] < ring_base[1],
        pinky_tip[1] < pinky_base[1],
    ]

    if all(fingers_extended):
        ws.send("LED ON")  # Light on
        return "Open Palm (Light ON)"

    if not any(fingers_extended):
        ws.send("LED OFF")  # Light off
        return "Closed Fist (Light OFF)"

    # Two fingers up for Fan ON, One finger up for Fan OFF
    if index_tip[1] < index_base[1] and middle_tip[1] < middle_base[1] and not ring_tip[1] < ring_base[1]:
        ws.send("FAN ON")  # Fan on
        return "Two Fingers Up (Fan ON)"

    if index_tip[1] < index_base[1] and not middle_tip[1] < middle_base[1]:
        ws.send("FAN OFF")  # Fan off
        return "One Finger Up (Fan OFF)"

    if thumb_tip[1] < index_base[1]:
        ws.send("VIDEO PLAY")  # Play video
        return "Thumbs Up (Video PLAY)"

    # **Pinch** for Video Pause (Volume Decrease) - thumb and index tip pinched together
    if thumb_tip[1] > index_base[1] and abs(thumb_tip[0] - index_tip[0]) < 20:
        ws.send("VIDEO PAUSE")  # Pause video
        return "Pinch (Video PAUSE)"

    # Additional gestures like Peace (Volume Decrease)
    if index_tip[1] < index_base[1] and middle_tip[1] < middle_base[1] and not ring_tip[1] < ring_base[1]:
        ws.send("VOLUME DOWN")  # Volume decrease
        return "Peace (Volume DOWN)"

    return "Unknown"

# Start video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] Camera not detected.")
    exit()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand detection
    results = hands.process(rgb_frame)
    gesture = "No Hand Detected"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            draw_extra_lines(frame, hand_landmarks.landmark)
            gesture = detect_gesture(hand_landmarks.landmark)

    # FPS Calculation
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time))
    prev_time = curr_time

    # Display Gesture and FPS
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, f"FPS: {fps}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Close the WebSocket connection
ws.close()
