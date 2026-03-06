from flask import Flask, render_template, request, jsonify
import cv2
from ultralytics import YOLO
import numpy as np
import base64
import torch
# Tries to use the GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Yolo model
model = YOLO("yolo26n-seg.pt")
# Transfers weights to the GPU if possible
model.to(device)

# Initializes web app
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video', methods=['POST'])

# Processes frame and sends it back to the client
def observe_frames():
    # Get the frame data from the request
    data = request.json
    frame_data = data['frame']

    # Splits the data in order to decode the Base64 string
    header, encoded = frame_data.split(",", 1)

    # Decodes the Base64 
    frame_bytes = base64.b64decode(encoded)

    # Puts the data into an array to make an image
    numpy_array = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

    # Processes the frame using YOLO
    results = model(frame, device=device)

    # Gets label for the most prevelant object
    detected_label = "Nothing Detected"
    if len(results[0].boxes) > 0:
        best_box = max(results[0].boxes, key=lambda box: box.conf[0])
        class_id = int(best_box.cls[0])
        detected_label = model.names[class_id]
    final_frame = results[0].plot()

    # Reencode the frame
    completed, buffer = cv2.imencode('.jpg', final_frame)
    if not completed:
        return jsonify({'error': 'Failed to reencode the frame'})
    encoded_frame = base64.b64encode(buffer).decode('utf-8')

    # Send the final frame back to the client
    return jsonify({'frame': f"data:image/jpeg;base64,{encoded_frame}", 'label': detected_label})

# Runs the web app
if __name__ == "__main__":
    app.run()
