# ======================================================================================
# Config
# ======================================================================================
from flask import Flask, render_template, request, jsonify
from hand_ctrl import *

app = Flask(__name__)
latest_result = {'hands_detected': False, 'hands': []}

# util
def get_latest():
    return latest_result

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