import os
import cv2
import json
import pickle
import face_recognition
import numpy as np

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(1)
# camera.set(3, 800)
# camera.set(4, 400)

PICKLES_DIR = "pickles"
facesList = []

def recognizeFace(image, face):
    print('HORA DO SHOOW')

    best_face_distance = 100
    name = ''
    face_encoding = face_recognition.face_encodings(image, [face])[0]

    for filename in os.listdir(PICKLES_DIR):
        with open(f"{PICKLES_DIR}/{filename}", 'rb') as f:
	        known_faces = pickle.load(f)

        label = os.path.splitext(filename)[0]
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        average_face_distances = np.average(face_distances)

        if (average_face_distances < best_face_distance):
            best_face_distance = average_face_distances
            name = label

    return name if best_face_distance < 0.6 else 'Unknown'

def findPreviousFace(top, right, bottom, left):
    for face in facesList:
        name, (prevTop, prevRight, prevBottom, prevLeft), tries = face
        magicNumber = abs(prevTop - top) + abs(prevRight - right) + abs(prevBottom - bottom) + abs(prevLeft - left)
        # if abs(prevTop - top) < 20 and abs(prevRight - right) < 20 and abs(prevBottom - bottom) < 20 and abs(prevLeft - left) < 20:
        if magicNumber < 80:
            return face
    return None

    
while camera.isOpened():
    ret, image = camera.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5, minSize = (30,30))
    
    newList = []
    for (x,y,w,h) in faces:
        top = y
        right = x+w
        bottom = y+h
        left = x
        face = (top, right, bottom, left)
        tries = 0

        previousFace = findPreviousFace(top, right, bottom, left)

        if previousFace is None:
            name = recognizeFace(image, face)
        else:
            name, prevFace, tries = previousFace
            if name == 'Unknown' and tries <= 30:
                if tries % 10 == 0:
                    name = recognizeFace(image, face)
                tries += 1

        newList.append((name, face, tries))

    facesList = newList
    for (name, face, tries) in facesList:
        top, right, bottom, left = face
        cv2.rectangle(image, (left,top), (right, bottom), (100,0,100), 2)
        cv2.putText(image, name.split('-')[0], (left,bottom),cv2.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)

    cv2.imshow('Image',image)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()