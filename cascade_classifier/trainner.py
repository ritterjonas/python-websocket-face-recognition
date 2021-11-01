import face_recognition
import pickle
import os

all_face_encodings = {}

DATASET_DIR = "dataset"
ACCEPTED_FILES = [".png", ".jpg", ".jpeg"]

for filename in os.listdir(DATASET_DIR):
    if (os.path.splitext(filename)[1] in ACCEPTED_FILES):
        label = os.path.splitext(filename)[0]
        print(f'training {label}')
        image = face_recognition.load_image_file(f"{DATASET_DIR}/{filename}")
        all_face_encodings[label] = face_recognition.face_encodings(image)[0]

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)