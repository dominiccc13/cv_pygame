import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from draw_lmks import draw_landmarks_on_image

# STEP 1: Create a handlandmarker object
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# STEP 2: Load the input image
image = mp.Image.create_from_file("woman_hands.jpg")

# STEP 3: Detect hand landmarks from the input image
detection_result = detector.detect(image)

# STEP 4: Process the classification result. in this case, visualize it
annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
while True:
    cv2.imshow("Hand Landmarks Result", annotated_image_bgr)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()