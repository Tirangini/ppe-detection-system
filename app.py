from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import csv
import os

app = Flask(__name__)
model = YOLO("best.pt")
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        results = model(frame, verbose=False)
        annotated_frame = results[0].plot()

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def get_violations():
    violations = []
    log_file = "violations/violations_log.csv"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            reader = csv.DictReader(f)
            violations = list(reader)
    return violations

@app.route('/')
def index():
    violations = get_violations()
    return render_template('index.html', violations=violations)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)