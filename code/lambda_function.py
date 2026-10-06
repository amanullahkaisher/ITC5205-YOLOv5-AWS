import json
import os
from pathlib import Path

import boto3
import cv2
import torch

s3 = boto3.client("s3")

BUCKET = os.environ.get("BUCKET_NAME", "itc5205-yolov5-kaiser")
INPUT_KEY = os.environ.get("INPUT_KEY", "input/download.jpg")
OUTPUT_KEY = os.environ.get("OUTPUT_KEY", "output/lambda-result.jpg")

# Load once per Lambda execution environment so warm invocations can reuse the model.
MODEL = torch.hub.load(
    "/var/task/yolov5",
    "yolov5s",
    source="local",
    pretrained=True
)

def lambda_handler(event, context):
    input_path = "/tmp/input.jpg"
    output_path = "/tmp/lambda-result.jpg"

    try:
        s3.download_file(BUCKET, INPUT_KEY, input_path)

        results = MODEL(input_path)
        detections = []
        for *xyxy, conf, cls in results.xyxy[0].cpu().numpy():
            detections.append({
                "object": results.names[int(cls)],
                "confidence": round(float(conf), 2)
            })

        # Render the annotated result deterministically to /tmp.
        rendered = results.render()
        if not rendered:
            raise RuntimeError("YOLOv5 returned no rendered image")

        bgr = cv2.cvtColor(rendered[0], cv2.COLOR_RGB2BGR)
        if not cv2.imwrite(output_path, bgr):
            raise RuntimeError("Failed to write annotated image")

        s3.upload_file(output_path, BUCKET, OUTPUT_KEY)

        body = {
            "status": "success",
            "message": "YOLOv5 detection completed by AWS Lambda",
            "detections": detections,
            "output": f"s3://{BUCKET}/{OUTPUT_KEY}"
        }
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body)
        }

    except Exception as exc:
        print(f"ERROR: {exc}", flush=True)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": str(exc)
            })
        }
