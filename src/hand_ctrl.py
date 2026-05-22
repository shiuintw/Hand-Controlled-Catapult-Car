# ======================================================================================
# Config
# ======================================================================================
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['ABSL_MIN_LOG_LEVEL'] = '2'

import cv2
import mediapipe as mp
import numpy as np
import math
import base64

# ======================================================================================
# MediaPipe Setup
# ======================================================================================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ======================================================================================
# Util Functions
# ======================================================================================
def get_angle(p1, p2, p3):
    angle = abs(
        math.degrees(
            math.atan2(p3[1] - p2[1], p3[0] - p2[0]) -
            math.atan2(p1[1] - p2[1], p1[0] - p2[0])
        )
    )
    return angle if angle <= 180 else 360 - angle

def decode_frame(data_url):
    # base64 data URL to OpenCV frame
    header, encoded = data_url.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    np_arr = np.frombuffer(img_bytes, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return frame

def analyze_hand(hand):
    # Finger Landmarks
    fingers = {
        'thumb':  get_angle(
            (hand.landmark[1].x, hand.landmark[1].y),
            (hand.landmark[2].x, hand.landmark[2].y),
            (hand.landmark[4].x, hand.landmark[4].y)
        ),
        'index':  get_angle(
            (hand.landmark[5].x, hand.landmark[5].y),
            (hand.landmark[6].x, hand.landmark[6].y),
            (hand.landmark[8].x, hand.landmark[8].y)
        ),
        'middle': get_angle(
            (hand.landmark[9].x,  hand.landmark[9].y),
            (hand.landmark[10].x, hand.landmark[10].y),
            (hand.landmark[12].x, hand.landmark[12].y)
        ),
        'ring':   get_angle(
            (hand.landmark[13].x, hand.landmark[13].y),
            (hand.landmark[14].x, hand.landmark[14].y),
            (hand.landmark[16].x, hand.landmark[16].y)
        ),
        'pinky':  get_angle(
            (hand.landmark[17].x, hand.landmark[17].y),
            (hand.landmark[18].x, hand.landmark[18].y),
            (hand.landmark[20].x, hand.landmark[20].y)
        ),
    }

    # Identification
    bent = {k: v < 160 for k, v in fingers.items()}

    if all(not b for b in bent.values()):
        gesture = 'open'
    elif all(bent.values()):
        gesture = 'fist'
    elif not bent['index'] and all(bent[f] for f in ['middle', 'ring', 'pinky']):
        gesture = 'point'
    elif not bent['thumb'] and all(bent[f] for f in ['index', 'middle', 'ring', 'pinky']):
        gesture = 'thumbs_up'
    else:
        gesture = 'unknown'

    return {
        'gesture': gesture,
        'angles': fingers,
        'bent': bent
    }

# === RETURN API ===
# {
#     'hands_detected': True,
#     'hands': [
#         {
#             'side': 'Left',
#             'gesture': 'open',
#             'angles': {
#                 'thumb': 170.3,
#                 'index': 165.2,
#                 'middle': 172.1,
#                 'ring': 168.4,
#                 'pinky': 160.8
#             },
#             'bent': {
#                 'thumb': False,
#                 'index': False,
#                 'middle': False,
#                 'ring': False,
#                 'pinky': False
#             },
#             'landmarks': [
#                 {'x': 0.52, 'y': 0.83, 'z': -0.01},
#                 ...  # 21 points total (0~20)
#             ]
#         },
#         {
#             'side': 'Right',
#             ...  # same structure
#         }
#     ]
# }
# === ========== ===
def process_hands(frame, hands):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    processed = hands.process(frame_rgb)

    result = {
        'hands_detected': False,
        'hands': []
    }

    if not processed.multi_hand_landmarks:
        return result

    result['hands_detected'] = True
    hands_with_label = []

    for hand, handedness in zip(
        processed.multi_hand_landmarks,
        processed.multi_handedness
    ):
        hand_data = analyze_hand(hand)
        hand_data['side'] = handedness.classification[0].label

        landmarks = []
        for lm in hand.landmark:
            landmarks.append({'x': lm.x, 'y': lm.y, 'z': lm.z})
        hand_data['landmarks'] = landmarks

        hands_with_label.append(hand_data)

    hands_with_label.sort(key=lambda h: 0 if h['side'] == 'Left' else 1)
    result['hands'] = hands_with_label

    return result