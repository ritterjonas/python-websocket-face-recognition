import cv2
import sys
import face_recognition
import numpy as np
import os
import base64

KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"
ACCEPTED_FILES = [".png", ".jpg", ".jpeg"]

class Camera(object):
    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.output_base64 = []
        self.video_capture = cv2.VideoCapture(0)

    def train(self):
        print("loading faces")
        for filename in os.listdir(KNOWN_FACES_DIR):
            if (os.path.splitext(filename)[1] in ACCEPTED_FILES):
                image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
                encoding = face_recognition.face_encodings(image)[0]
                self.known_faces.append(encoding)
                self.known_names.append(os.path.splitext(filename)[0])
        print("faces loaded")

    def process(self):

        if self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
            rgb_small_frame = small_frame[:, :, ::-1]

            self.face_locations = face_recognition.face_locations(rgb_small_frame, model="hog") #cnn
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []

            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                name = "Amigão"

                face_distances = face_recognition.face_distance(self.known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_names[best_match_index]

                self.face_names.append(name)
            
            self.output_base64 = []

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 3
                right *= 3
                bottom *= 3
                left *= 3
                x = int((bottom - top) / 2)
                top_cropped = top - x
                right_cropped = right + x
                bottom_cropped = bottom + x
                left_cropped = left - x
                face_image = frame[top_cropped:bottom_cropped, left_cropped:right_cropped]

                if face_image.any():
                    face_image_resized = cv2.resize(face_image, (256,256))
                    retval, buffer = cv2.imencode('.jpg', face_image_resized)
                    base64_image = base64.b64encode(buffer).decode()
                    self.output_base64.append({ "name": name, "image": base64_image })
        
        return self.output_base64
