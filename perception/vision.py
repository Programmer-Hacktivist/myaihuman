import cv2
from deepface import DeepFace

AUTHORIZED_USER = "Max"

def detect_face_and_emotion():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None, None

    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
    except:
        emotion = "unknown"

    # Face recognition placeholder (expand later)
    user = AUTHORIZED_USER

    return user, emotion
