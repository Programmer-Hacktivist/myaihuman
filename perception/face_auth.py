import face_recognition
import cv2
import pickle
import os

ENCODINGS_FILE = "face_encodings.pkl"

def register_face(name="Max"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    rgb = frame[:, :, ::-1]
    encodings = face_recognition.face_encodings(rgb)

    if not encodings:
        print("No face detected")
        return

    data = {"name": name, "encoding": encodings[0]}

    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    print("Face registered")


def authenticate():
    if not os.path.exists(ENCODINGS_FILE):
        return False

    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    rgb = frame[:, :, ::-1]
    encodings = face_recognition.face_encodings(rgb)

    for encoding in encodings:
        match = face_recognition.compare_faces([data["encoding"]], encoding)
        if match[0]:
            return True

    return False
