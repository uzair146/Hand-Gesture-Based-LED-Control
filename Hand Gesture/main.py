"""
DLD Lab Project - Hand Gesture Based LED Control
2nd Semester - Digital Logic Design

Description:
    Detects number of raised fingers using webcam + MediaPipe,
    sends count to Arduino via Serial to control LEDs (0-5).

Requirements:
    pip install opencv-python mediapipe==0.10.13 pyserial

Hardware:
    - Arduino (connected via USB)
    - 5 LEDs on Arduino pins (as per your circuit diagram)

Usage:
    python main.py                   # With Arduino on COM6
    python main.py --port COM3       # Different COM port
    python main.py --no-arduino      # Demo mode (no hardware needed)

Controls:
    Press 'q' to quit
"""

import cv2
import mediapipe as mp
import time
import argparse
import sys

# ─── Argument Parser ────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Hand Gesture LED Controller - DLD Project")
parser.add_argument(
    "--no-arduino",
    action="store_true",
    help="Run in demo mode without Arduino connected"
)
parser.add_argument(
    "--port",
    type=str,
    default="COM6",
    help="Serial port for Arduino (default: COM6). Linux/Mac: /dev/ttyUSB0"
)
parser.add_argument(
    "--baud",
    type=int,
    default=9600,
    help="Baud rate (default: 9600, must match Arduino sketch)"
)
args = parser.parse_args()

# ─── Arduino Setup ──────────────────────────────────────────────────────────
Arduino = None

if not args.no_arduino:
    try:
        import serial
        Arduino = serial.Serial(port=args.port, baudrate=args.baud, timeout=1)
        time.sleep(2)  # Allow Arduino to reset after serial connection
        print(f"[OK] Arduino connected on {args.port} at {args.baud} baud")
    except Exception as e:
        print(f"[WARNING] Arduino not found: {e}")
        print("[INFO] Continuing in demo mode (no LEDs). Use --no-arduino to skip this warning.")
else:
    print("[INFO] Demo mode: Arduino disabled")

# ─── MediaPipe Setup ────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# ─── Webcam Setup ───────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] Cannot open webcam. Make sure a camera is connected.")
    sys.exit(1)

print("[OK] Webcam opened. Press 'q' to quit.")

# MediaPipe landmark IDs for fingertips
# 4=Thumb, 8=Index, 12=Middle, 16=Ring, 20=Pinky
FINGER_TIP_IDS = [4, 8, 12, 16, 20]

prev_fingers_up = -1  # Avoid redundant serial writes

# ─── Main Loop ──────────────────────────────────────────────────────────────
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to read from webcam.")
        break

    frame = cv2.flip(frame, 1)           # Mirror for natural feel
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    fingers_up = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            # Thumb: use X axis (horizontal comparison)
            if lm[FINGER_TIP_IDS[0]].x < lm[FINGER_TIP_IDS[0] - 1].x:
                fingers_up += 1

            # Index, Middle, Ring, Pinky: use Y axis (tip above 2nd joint = extended)
            for i in range(1, 5):
                if lm[FINGER_TIP_IDS[i]].y < lm[FINGER_TIP_IDS[i] - 2].y:
                    fingers_up += 1

        # Send to Arduino only on change (reduces serial noise)
        if Arduino and fingers_up != prev_fingers_up:
            try:
                Arduino.write(str(fingers_up).encode())
                prev_fingers_up = fingers_up
            except Exception as e:
                print(f"[WARNING] Serial write failed: {e}")

    else:
        # No hand — send 0, turn off all LEDs
        fingers_up = 0
        if Arduino and prev_fingers_up != 0:
            try:
                Arduino.write(b'0')
                prev_fingers_up = 0
            except Exception as e:
                print(f"[WARNING] Serial write failed: {e}")

    # ── On-Screen UI ──
    # Dark background panel for text
    cv2.rectangle(frame, (10, 10), (310, 85), (0, 0, 0), -1)
    cv2.putText(frame, f"Fingers Up: {fingers_up}", (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2)
    mode = "DEMO" if Arduino is None else f"LIVE ({args.port})"
    cv2.putText(frame, f"Mode: {mode}", (20, 78),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

    # Virtual LED indicators
    for i in range(5):
        color = (0, 255, 50) if i < fingers_up else (50, 50, 50)
        cx = w - 55 - i * 55
        cv2.circle(frame, (cx, 50), 20, color, -1)
        cv2.putText(frame, f"L{i+1}", (cx - 12, 56),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

    cv2.imshow("Hand Gesture LED Controller | DLD Project | Press Q to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Quit.")
        break

# ─── Cleanup ────────────────────────────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
if Arduino:
    Arduino.close()
    print("[INFO] Arduino disconnected.")
print("[INFO] Done.")
