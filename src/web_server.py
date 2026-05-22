# ======================================================================================
# Config
# ======================================================================================
from flask import Flask, render_template, request, jsonify
from hand_ctrl import *

app = Flask(__name__)

# ======================================================================================
# Routes
# ======================================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_frame():
    data = request.json
    if not data or 'frame' not in data:
        return jsonify({'error': 'No frame data'}), 400

    frame = decode_frame(data['frame'])
    if frame is None:
        return jsonify({'error': 'Failed to decode frame'}), 400

    return jsonify(process_hands(frame, hands))

# ======================================================================================
# Run
# ======================================================================================
if __name__ == '__main__':
    print("Server running at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)