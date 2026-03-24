import cv2
import mediapipe as mp
import time
import numpy as np
import pyautogui
import os
import winsound

# ------------------ SETTINGS ------------------
pyautogui.FAILSAFE = False

BASE_DIR = "gesture-recognition"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

cooldown = 2
last_capture_time = 0

action_delay = 0.4
last_action_time = 0

gesture_buffer = []
buffer_size = 7
stable_gesture = "None"

screenshot_type = "Full"

screen_w, screen_h = pyautogui.size()

# -------- MOUSE SMOOTHING --------
prev_x, prev_y = 0, 0
alpha = 0.2  # smoothing factor (lower = smoother)

# ------------------ MEDIAPIPE ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

pTime = 0
mode = "Normal Mode"

# ------------------ FUNCTIONS ------------------

def detect_fingers(landmarks):
    fingers = []

    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    tips = [8, 12, 16, 20]
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def get_gesture(fingers):
    total = sum(fingers)

    if total == 0:
        return "Fist"
    elif total == 5:
        return "Open Palm"
    elif total == 2 and fingers[1] and fingers[2]:
        return "Peace"
    elif fingers[0] == 1 and total == 1:
        return "Thumbs Up"
    elif fingers[1] == 1 and total == 1:
        return "Point"
    else:
        return "Unknown"


# ------------------ MAIN LOOP ------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "No Hand"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            h, w, _ = frame.shape

            fingers = detect_fingers(landmarks)
            gesture = get_gesture(fingers)

            # -------- STABLE GESTURE --------
            gesture_buffer.append(gesture)
            if len(gesture_buffer) > buffer_size:
                gesture_buffer.pop(0)

            stable_gesture = max(set(gesture_buffer), key=gesture_buffer.count)

            current_time = time.time()

            # -------- MODE SWITCH --------
            if current_time - last_action_time > 0.8:
                if stable_gesture == "Peace":
                    mode = "Volume Mode"
                    last_action_time = current_time

                elif stable_gesture == "Thumbs Up":
                    mode = "Screenshot Mode"
                    last_action_time = current_time

                elif stable_gesture == "Fist":
                    mode = "Mouse Mode"
                    last_action_time = current_time

                elif stable_gesture == "Open Palm":
                    mode = "Normal Mode"
                    last_action_time = current_time

            # -------- VOLUME --------
            if mode == "Volume Mode":
                x1 = int(landmarks[4].x * w)
                y1 = int(landmarks[4].y * h)
                x2 = int(landmarks[8].x * w)
                y2 = int(landmarks[8].y * h)

                length = np.hypot(x2 - x1, y2 - y1)

                if current_time - last_action_time > action_delay:
                    if length > 150:
                        pyautogui.press("volumeup")
                    elif length < 50:
                        pyautogui.press("volumedown")

                    last_action_time = current_time

                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # -------- SCREENSHOT --------
            if mode == "Screenshot Mode":

                if stable_gesture == "Peace":
                    screenshot_type = "Window"

                if stable_gesture in ["Thumbs Up", "Point"]:
                    if current_time - last_capture_time > cooldown:

                        filename = os.path.join(
                            SCREENSHOT_DIR,
                            f"{screenshot_type}_{int(current_time)}.png"
                        )

                        if screenshot_type == "Full":
                            screenshot = pyautogui.screenshot()
                            screenshot.save(filename)
                        else:
                            cv2.imwrite(filename, frame)

                        winsound.Beep(1000, 200)

                        last_capture_time = current_time

                        cv2.putText(frame, "Screenshot Saved", (100, 220),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)

            # -------- ULTRA SMOOTH MOUSE --------
            if mode == "Mouse Mode":

                # raw position
                raw_x = np.interp(landmarks[8].x, [0.2, 0.8], [0, screen_w])
                raw_y = np.interp(landmarks[8].y, [0.2, 0.8], [0, screen_h])

                # smoothing (EMA)
                prev_x = prev_x + alpha * (raw_x - prev_x)
                prev_y = prev_y + alpha * (raw_y - prev_y)

                pyautogui.moveTo(prev_x, prev_y)

                # click detection
                x1 = int(landmarks[4].x * w)
                y1 = int(landmarks[4].y * h)
                x2 = int(landmarks[8].x * w)
                y2 = int(landmarks[8].y * h)

                distance = np.hypot(x2 - x1, y2 - y1)

                if distance < 45:
                    if current_time - last_action_time > 0.6:
                        pyautogui.click()
                        last_action_time = current_time

    # -------- FPS --------
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    # -------- UI --------
    color = (0, 255, 0)
    if stable_gesture == "Thumbs Up":
        color = (0, 255, 255)
    elif stable_gesture == "Peace":
        color = (255, 0, 0)
    elif stable_gesture == "Fist":
        color = (0, 0, 255)

    cv2.rectangle(frame, (10, 10), (520, 180), (0, 0, 0), -1)

    cv2.putText(frame, f"Gesture: {stable_gesture}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3)

    cv2.putText(frame, f"Mode: {mode}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(frame, f"Shot Type: {screenshot_type}", (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.imshow("Gesture HCI System (Ultra Smooth)", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()