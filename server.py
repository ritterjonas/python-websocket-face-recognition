from flask import Flask, render_template
from flask_socketio import SocketIO
from time import sleep
import cv2
import json
import base64
from camera import Camera

app = Flask(__name__)
app.config['SECRET_KEY'] = '78581099#lkjh'
socketio = SocketIO(app)
camera = Camera()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('check')
def gen(req):
    while True:
        data = camera.process()
        socketio.emit('image', data)
        socketio.sleep(0)

if __name__== "__main__":
    camera.train()
    socketio.run(app, debug=True, host='127.0.0.1', port=5000) 	
