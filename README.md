Real-Time Hand Gesture Recognition System
📌 Overview
This project implements a real-time hand gesture recognition system
using computer vision techniques. It detects hand movements through a
webcam and maps gestures to useful system actions.
The system is built using MediaPipe for hand tracking and OpenCV for
image processing.
---
🚀 Features
Real-time hand detection and tracking\
Finger counting using hand landmarks\
Gesture recognition (Fist, Open Palm, Peace, Thumbs Up)\
Volume control using finger distance\
Screenshot capture using gesture\
Live FPS display for performance monitoring\
Clean user interface with visual feedback
---
🛠️ Technologies Used
Python\
OpenCV\
MediaPipe\
NumPy\
PyAutoGUI
---
⚙️ How It Works
The webcam captures live video input\
MediaPipe detects hand landmarks (21 key points)\
Finger positions are analyzed\
Gestures are identified based on finger states\
Gestures are mapped to system actions
---
▶️ Installation
``` bash
git clone https://github.com/PLKR-21/gesture-recognition-system.git
cd gesture-recognition-system
pip install opencv-python mediapipe numpy pyautogui
```
---
▶️ Usage
``` bash
python gesture.py
```
---
🎯 Gesture Controls
Gesture              Action
---
👍 Thumbs Up         Capture Screenshot
✋ Open Palm         Detection Active
✌️ Peace             Recognition Mode
✊ Fist              Reset / Neutral
🤏 Finger Distance   Volume Control
---
📊 Output
Real-time gesture detection on screen\
Volume changes using hand movement\
Screenshot saved in project directory\
FPS displayed
---
👨‍💻 Author
P. Laxmi Kanth Reddy  
B.Tech Computer Science
---
⭐ Conclusion
This project demonstrates real-time human-computer interaction using
computer vision.
