from flask import Flask, jsonify, request, redirect
import os
import cv2
import json
import pickle
import face_recognition
import numpy as np

PICKLES_DIR = "pickles"

class Camera(object):
    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.output_base64 = []
        self.video_capture = cv2.VideoCapture(0)

    def detect_faces(self, file_stream):
        img = face_recognition.load_image_file(file_stream)
        self.face_encodings = face_recognition.face_encodings(img)

        self.face_names = []

        for face_encoding in self.face_encodings:
            best_face_distance = 100
            name = ''

            for filename in os.listdir(PICKLES_DIR):
                with open(f"{PICKLES_DIR}/{filename}", 'rb') as f:
                    known_faces = pickle.load(f)

                label = os.path.splitext(filename)[0]
                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                average_face_distances = np.average(face_distances)

                if (average_face_distances < best_face_distance):
                    best_face_distance = average_face_distances
                    name = label

            if best_face_distance < 0.6:
                self.face_names.append(name)

        self.face_names.sort()
        return jsonify(list(dict.fromkeys(self.face_names)))


def recognizeFace(image, face):
    best_face_distance = 100
    name = ''
    face_encoding = face_recognition.face_encodings(image, [face])[0]

