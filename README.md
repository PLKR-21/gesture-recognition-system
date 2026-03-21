# Real-Time Hand Gesture Recognition System

## 📌 Overview
This project implements a real-time hand gesture recognition system using computer vision techniques. It detects hand movements through a webcam and maps gestures to useful system actions.

The system is built using MediaPipe for hand tracking and OpenCV for image processing.

---

## 🚀 Features
- Real-time hand detection and tracking  
- Finger counting using hand landmarks  
- Gesture recognition (Fist, Open Palm, Peace, Thumbs Up)  
- Volume control using finger distance  
- Screenshot capture using gesture  
- Live FPS display for performance monitoring  
- Clean user interface with visual feedback  

---

## 🛠️ Technologies Used
- Python  
- OpenCV  
- MediaPipe  
- NumPy  
- PyAutoGUI  

---

## ⚙️ How It Works
1. The webcam captures live video input  
2. MediaPipe detects hand landmarks (21 key points)  
3. Finger positions are analyzed  
4. Gestures are identified based on finger states  
5. Gestures are mapped to system actions like volume control and screenshot capture  

---

## ▶️ Installation

```bash
git clone https://github.com/PLKR-21/gesture-recognition-system.git
cd gesture-recognition-system
pip install opencv-python mediapipe numpy pyautogui
