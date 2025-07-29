import cv2
import mediapipe as mp
import serial
import time

# serial setup
arduino = serial.Serial('COM11', 9600)  # change to your arduino port
time.sleep(2)

# mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# webcam
cap = cv2.VideoCapture(0)

def fingers_up(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    fingers = []

    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

prev_command = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = fingers_up(hand_landmarks)
            total_fingers = sum(fingers)

            if total_fingers >= 4:
                command = 'ON'
            elif total_fingers <= 1:
                command = 'OFF'
            else:
                command = None

            if command and command != prev_command:
                arduino.write((command + '\n').encode())
                prev_command = command
                print(f"Sent to Arduino: {command}")

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
