# Face Tracking Laser Turret Using OpenCV 🔴🎯

A computer vision–based laser turret system that tracks a human face using OpenCV and sends servo angle coordinates to Arduino for real-time laser targeting.

## 🔧 Technologies Used

- Python (OpenCV for face detection)
- Arduino (Servo motor control)
- Serial Communication (Python ↔ Arduino)
- Haar Cascade Classifier

## 🧠 Key Features

- Real-time face detection using webcam
- Tracks the **largest face** in the frame
- Sends coordinates to Arduino over serial to align servos
- Safe fallback when no face is detected

## 📁 Project Structure
Face-Tracking-Laser-Turret/
├── Face_detection.py # Python OpenCV script
├── servo.ino # Arduino code for servo movement


## 🚀 How to Run

1. **Upload** `servo.ino` to your Arduino board.
2. **Connect webcam** and ensure the correct COM port is set in `Face_detection.py`.
3. Run the Python script:


Prerequisites
Python 3.x

OpenCV installed (pip install opencv-python)

PySerial installed (pip install pyserial)

Arduino IDE (for uploading .ino)
