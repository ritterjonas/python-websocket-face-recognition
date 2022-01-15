from flask import Flask, render_template, request
import cv2
from camera import Camera

app = Flask(__name__)
camera = Camera()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def upload_image():
    file = request.files['file']
    return camera.detect_faces(file)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
