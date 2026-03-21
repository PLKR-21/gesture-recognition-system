import cv2
import mediapipe as mp
import time
import numpy as np
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

pTime = 0

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
    elif total == 2 and fingers[1] == 1 and fingers[2] == 1:
        return "Peace"
    elif fingers[0] == 1 and total == 1:
        return "Thumbs Up"
    else:
        return "Unknown"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "No Hand"
    finger_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            h, w, _ = frame.shape

            fingers = detect_fingers(landmarks)
            finger_count = sum(fingers)
            gesture = get_gesture(fingers)

            # Volume control using finger distance
            x1 = int(landmarks[4].x * w)
            y1 = int(landmarks[4].y * h)
            x2 = int(landmarks[8].x * w)
            y2 = int(landmarks[8].y * h)

            length = np.hypot(x2 - x1, y2 - y1)

            # Control volume using distance
            if length > 150:
                pyautogui.press("volumeup")
            elif length < 50:
                pyautogui.press("volumedown")

            # Draw line between fingers
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # Screenshot
            if gesture == "Thumbs Up":
                cv2.imwrite("screenshot.png", frame)
                cv2.putText(frame, "Screenshot Saved", (200, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    # UI
    cv2.rectangle(frame, (10, 10), (420, 120), (0, 0, 0), -1)

    cv2.putText(frame, f"Gesture: {gesture}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(frame, f"Fingers: {finger_count}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

    cv2.imshow("Advanced Gesture Control System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()