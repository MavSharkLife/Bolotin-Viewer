from flask import Flask, render_template, request, jsonify
import cv2
from ultralytics import YOLO
import numpy as np
import base64
import torch
# tries to use the gpu
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Yolo model
model = YOLO("yolo26n-seg.pt")
# transfers weights to the gpu if possible
model.to(device)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video', methods=['POST'])


def observe_frames():
    # get the frame data from the request
    data = request.json
    frame_data = data['frame']

    # splits the data in order to decode the base64 string
    header, encoded = frame_data.split(",", 1)

    # decodes the base64 
    frame_bytes = base64.b64decode(encoded)

    # puts it into an array to make an image
    numpy_array = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

    # process the frame
    results = model(frame, device=device)

    detected_label = "Nothing Detected"
    if len(results[0].boxes) > 0:
        best_box = max(results[0].boxes, key=lambda box: box.conf[0])
        class_id = int(best_box.cls[0])
        detected_label = model.names[class_id]


    final_frame = results[0].plot()

    # reencode the frame
    completed, buffer = cv2.imencode('.jpg', final_frame)
    if not completed:
        return jsonify({'error': 'Failed to reencode the frame'})
    encoded_frame = base64.b64encode(buffer).decode('utf-8')

    # send it back 
    return jsonify({'frame': f"data:image/jpeg;base64,{encoded_frame}", 'label': detected_label})


if __name__ == "__main__":
    app.run(debug=True)