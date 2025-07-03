import cv2
import serial
import time

# Load the pre-trained Haar Cascade face detector from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture from the default webcam (0)ṇ
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Press 'q' to quit.")

# Open serial connection to Arduino
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)  # Wait for connection to initialize
    print("Arduino connected.")
except serial.SerialException:
    print("Error: Could not connect to Arduino.")
    arduino = None

# Track last time data was sent
last_sent_time = 0
send_interval = 0.5  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 1: Detect all faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Step 2: Select the biggest face
    if len(faces) > 0:
        biggest_face = max(faces, key=lambda rect: rect[2] * rect[3])  # rect = (x, y, w, h)
        (x, y, w, h) = biggest_face

        # Step 3: Draw rectangle for the selected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print(f"Target Face at X:{x}, Y:{y}, Width:{w}, Height:{h}")

        # Step 4: Calculate center
        target_x = x + (w // 6)
        target_y = y + (h // 2)

        current_time = time.time()
        if current_time - last_sent_time >= send_interval:
            if arduino is not None:
                try:
                    message = f"{target_x},{target_y}\n"
                    arduino.write(message.encode('utf-8'))
                    print(f"Sent to Arduino: {message.strip()}")
                except serial.SerialException:
                    print("Error: Failed to send data to Arduino.")
            # else:
                # print(f"Arduino not connected. Target coordinates: {target_x},{target_y}")
            last_sent_time = current_time
    else:
        print("No face detected.")

    # Draw all face boxes (optional)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # Show the frame
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

if arduino is not None:
    arduino.close()
