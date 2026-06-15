# ======================================================================================
# Config
# ======================================================================================
from flask import Flask, render_template, request, jsonify
from hand_ctrl import *

app = Flask(__name__)
latest_result = {'hands_detected': False, 'hands': []}
latest_steer = 0
latest_speed = 0
latest_gripping = False
latest_lever = False

# util
def get_latest():
    return latest_result

def get_steer():
    return latest_steer

def get_speed():
    return latest_speed

def get_gripping():
    return latest_gripping

def get_lever():
    return latest_lever

# ======================================================================================
# Picamera2
# ======================================================================================
from flask import Response
import cv2

# 只在 RPi 上 import
try:
    from picamera2 import Picamera2
    picam = Picamera2()
    picam.configure(picam.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    ))
    picam.start()
    PICAM_OK = True
except Exception as e:
    print("Picamera2 not available:", e)
    PICAM_OK = False

def gen_frames():
    while True:
        frame = picam.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/picam')
def picam_feed():
    if not PICAM_OK:
        return "Picamera2 not available", 503
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ======================================================================================
# Routes
# ======================================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_frame():
    global latest_result
    data = request.json
    if not data or 'frame' not in data:
        return jsonify({'error': 'No frame data'}), 400

    frame = decode_frame(data['frame'])
    if frame is None:
        return jsonify({'error': 'Failed to decode frame'}), 400

    latest_result = process_hands(frame, hands)
    return jsonify(latest_result)

@app.route('/steer', methods=['POST'])
def steer():
    global latest_steer, latest_speed, latest_gripping, latest_lever
    data = request.json
    if data:
        latest_steer = max(-90, min(90, int(data.get('angle', 0))))
        latest_speed = max(-100, min(100, int(data.get('speed', 0))))
        latest_gripping = data.get('gripping', False)
        latest_lever = data.get('lever_gripping', False)
    return jsonify({'ok': True})

# ======================================================================================
# Run
# ======================================================================================
def web_boot():
    print("Server running at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

# ======================================================================================
# Test
# ======================================================================================
if __name__ == '__main__':
    web_boot()