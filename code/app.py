from flask import Flask, request, jsonify
from pathlib import Path
import torch

app = Flask(__name__)
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

@app.post("/detect")
def detect():
    if "file" not in request.files:
        return jsonify({"error": "file is required"}), 400

    upload = request.files["file"]
    path = Path("/tmp") / (upload.filename or "input.jpg")
    upload.save(path)

    results = model(str(path))
    detections = []
    for *xyxy, conf, cls in results.xyxy[0].cpu().numpy():
        detections.append({
            "object": results.names[int(cls)],
            "confidence": round(float(conf), 2)
        })

    return jsonify({"status": "success", "detections": detections})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
