import face_recognition
import pickle
import os

all_face_encodings = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "dataset")

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            path = os.path.join(root, file)
            label = os.path.basename(root)
            print(f'Training {label}')
            img = face_recognition.load_image_file(path)
            all_face_encodings[label] = face_recognition.face_encodings(img)[0]

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)