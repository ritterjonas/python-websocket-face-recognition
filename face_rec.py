import http.server as http
import asyncio
import websockets
import socketserver
import multiprocessing
import cv2
import sys
from datetime import datetime as dt
import face_recognition
import numpy as np
import os
import base64
import json

# Keep track of our processes
PROCESSES = []
KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"
ACCEPTED_FILES = [".png", ".jpg", ".jpeg"]

def log(message):
    print("[LOG] " + str(dt.now()) + " - " + message)

def camera(man):
    log("Starting camera")
    known_faces = []
    known_names = []
    face_locations = []
    face_encodings = []
    face_names = []

    output_base64 = []

    log("loading faces")
    for filename in os.listdir(KNOWN_FACES_DIR):
        if (os.path.splitext(filename)[1] in ACCEPTED_FILES):
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(os.path.splitext(filename)[0])
    log("faces loaded")

    video_capture = cv2.VideoCapture(0)

    process_this_frame_counter = 0

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame_counter > 10:
            process_this_frame_counter = 0
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog") #cnn
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "Amigão"

                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                face_names.append(name)
        
        process_this_frame_counter += 1
        output_base64 = []

        for (top, right, bottom, left), name in zip(face_locations, face_names):
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
                #cv2.imshow(name, face_image_resized)
                retval, buffer = cv2.imencode('.jpg', face_image_resized)
                base64_image = base64.b64encode(buffer).decode()
                output_base64.append([name, base64_image])

            #cv2.rectangle(frame, (left , top), (right, bottom), (0, 0, 255), 2)
            #font = cv2.FONT_HERSHEY_DUPLEX
            #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 65]
        man[0] = output_base64
    
    video_capture.release()
    cv2.destroyAllWindows()

# HTTP server handler
def server():
    server_address = ('0.0.0.0', 8000)
    if sys.version_info[1] < 7:
        class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.HTTPServer):
            pass
        httpd = ThreadingHTTPServer(server_address, http.SimpleHTTPRequestHandler)
    else:
        httpd = http.ThreadingHTTPServer(server_address, http.SimpleHTTPRequestHandler)
    log("Server started")
    httpd.serve_forever()

def socket(man):
    # Will handle our websocket connections
    async def handler(websocket, path):
        log("Socket opened")
        try:
            while True:
                await asyncio.sleep(0.1) # 30 fps
                await websocket.send(json.dumps(man[0]))
        except websockets.exceptions.ConnectionClosed:
            log("Socket closed")

    log("Starting socket handler")
    # Create the awaitable object
    start_server = websockets.serve(ws_handler=handler, host='0.0.0.0', port=8585)
    # Start the server, add it to the event loop
    asyncio.get_event_loop().run_until_complete(start_server)
    # Registered our websocket connection handler, thus run event loop forever
    asyncio.get_event_loop().run_forever()


def main():
    # queue = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    lst = manager.list()
    lst.append(None)
    # Host the page, creating the server
    http_server = multiprocessing.Process(target=server)
    # Set up our websocket handler
    socket_handler = multiprocessing.Process(target=socket, args=(lst,))
    # Set up our camera
    camera_handler = multiprocessing.Process(target=camera, args=(lst,))
    # Add 'em to our list
    PROCESSES.append(camera_handler)
    PROCESSES.append(http_server)
    PROCESSES.append(socket_handler)
    for p in PROCESSES:
        p.start()
    # Wait forever
    while True:
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        for p in PROCESSES:
            p.terminate()