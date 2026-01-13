import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 3000)

def send_command(cmd, sprinting):
    msg = f"{cmd},{sprinting}".encode()
    sock.sendto(msg, server_address)

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:
    # cv2 boilerplate
    ret, frame = cap.read()
    if not ret:
        break

    # prep image for machine learning and send to model
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    detection_result = detector.detect(mp_image)

    # handle hands and landmarks
    if detection_result.hand_landmarks:
        # initialize hand variables to determine direction
        hand1 = detection_result.hand_landmarks[0]
        hand1_dir = detection_result.handedness[0][0]
        left_hand = hand1 if hand1_dir.display_name == "Left" else None
        right_hand = hand1 if not left_hand else None

        if len(detection_result.handedness) > 1:
            if not left_hand:
                left_hand = detection_result.hand_landmarks[1]
            elif not right_hand:
                right_hand = detection_result.hand_landmarks[1]
        
        # handle forward movement
        if left_hand and right_hand:
            distance = left_hand[0].y - right_hand[0].y
            left_distance = left_hand[0].y - left_hand[12].y
            right_distance = right_hand[0].y - right_hand[12].y

            # determine if sprinting
            if left_distance < .25 or right_distance < .25:
                sprinting = True
            else:
                sprinting = False

            # determine if moving straight or diagonally
            # output movement + sprinting state
            if distance < -.25:
                print("sprinting: ", sprinting, " wa")
                send_command("wa", sprinting)
            elif distance > .25:
                print("sprinting: ", sprinting, " wd")
                send_command("wd", sprinting)
            else:
                send_command("w", sprinting)
                print("sprinting: ", sprinting, " w")

        # handle leftward movement
        if left_hand and not right_hand:
            distance = left_hand[0].y - left_hand[12].y
            sprinting = True if distance < .25 else False
            send_command("a", sprinting)
            print("a ", sprinting)

        # handle rightward movement
        if not left_hand and right_hand:
            distance = right_hand[0].y - right_hand[12].y
            sprinting = True if distance < .25 else False
            send_command("d", sprinting)
            print("d ", sprinting)

        # handle backward movement
        

        # display landmarks
        for hand in detection_result.hand_landmarks:
            # all points are contained within hand
            for landmark in hand:
                h, w, _ = frame.shape
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    cv2.imshow('Live Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()