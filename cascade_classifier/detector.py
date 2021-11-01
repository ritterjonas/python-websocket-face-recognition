import cv2
import json
import pickle
import face_recognition
import numpy as np

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)

with open('dataset_faces.dat', 'rb') as f:
	all_face_encodings = pickle.load(f)

known_names = list(all_face_encodings.keys())
known_faces = np.array(list(all_face_encodings.values()))

facesList = []

def recognizeFace(image, face):
    face_encoding = face_recognition.face_encodings(image, [face])[0]
    matches = face_recognition.compare_faces(known_faces, face_encoding)
    name = "Unknown"

    face_distances = face_recognition.face_distance(known_faces, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_names[best_match_index]

    return name

def findPreviousFace(top, right, bottom, left):
    for face in facesList:
        name, (prevTop, prevRight, prevBottom, prevLeft) = face
        magicNumber = abs(prevTop - top) + abs(prevRight - right) + abs(prevBottom - bottom) + abs(prevLeft - left)
        # if abs(prevTop - top) < 20 and abs(prevRight - right) < 20 and abs(prevBottom - bottom) < 20 and abs(prevLeft - left) < 20:
        if magicNumber < 80:
            return face
    return None

    
while camera.isOpened():
    ret, image = camera.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (30,30))
    
    newList = []
    for (x,y,w,h) in faces:
        top = y
        right = x+w
        bottom = y+h
        left = x
        face = (top, right, bottom, left)

        previousFace = findPreviousFace(top, right, bottom, left)

        if previousFace is None:
            print('BORA PESAR SAPORRA')
            name = recognizeFace(image, face)
        else:
            name, prevFace = previousFace

        newList.append((name, face))
    print(newList)
    facesList = newList
    for (name, face) in facesList:
        top, right, bottom, left = face
        cv2.rectangle(image, (left,top), (right, bottom), (100,0,100), 2)
        cv2.putText(image, name, (left,bottom),cv2.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)

    cv2.imshow('Image',image)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()