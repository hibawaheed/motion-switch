import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
tip_ids = [4, 8, 12, 16, 20]

def get_finger_status(hand_landmarks, hand_label):
    fingers = []
    #check x-axis instead of y-axis
    if hand_label == "Right":
        fingers.append(hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x)
    else:
        fingers.append(hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x)
    #check y-axis
    for id in range(1, 5):
        fingers.append(hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y)
    return fingers

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        hand_info = {"Left": None, "Right": None}

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = handedness.classification[0].label
                hand_info[label] = hand_landmarks

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                #labels
                for i, id in enumerate(tip_ids):
                    cx = int(hand_landmarks.landmark[id].x * image.shape[1])
                    cy = int(hand_landmarks.landmark[id].y * image.shape[0])
                    cv2.putText(image, f'{finger_names[i]}', (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        #right_primary
        active_hand = None
        if hand_info["Right"]:
            active_hand = ("Right", hand_info["Right"])
        elif hand_info["Left"]:
            active_hand = ("Left", hand_info["Left"])

        if active_hand:
            label, landmarks = active_hand
            status = get_finger_status(landmarks, label)
            #example
            on_off = "ON" if status[1] else "OFF"  #index
            cv2.putText(image, f"{label} Hand Control: {on_off}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        cv2.imshow('Hand Tracker', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
