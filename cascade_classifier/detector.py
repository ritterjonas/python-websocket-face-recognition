import cv2
import json
import pickle
import face_recognition
import numpy as np

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(1)

with open('dataset_faces.dat', 'rb') as f:
	all_face_encodings = pickle.load(f)

known_names = list(all_face_encodings.keys())
known_faces = np.array(list(all_face_encodings.values()))
    
while camera.isOpened():
    ret, image = camera.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (30,30))
    

    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x,y), (x+w, y+h), (100,0,100), 2)
        face_encoding = face_recognition.face_encodings(image, [(y,x+w,y+h,x)])[0]
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]

        cv2.putText(image, name, (x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)

    cv2.imshow('Image',image)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()