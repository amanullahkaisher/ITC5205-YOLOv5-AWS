#!/usr/bin/env bash
set -e

REGION="us-east-1"
ACCOUNT_ID="447567360091"
REPO="itc5205-yolov5-kaiser"
IMAGE="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO}:latest"

aws ecr get-login-password --region "$REGION" | \
docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

docker build -t "$REPO" ../code
docker tag "$REPO:latest" "$IMAGE"
docker push "$IMAGE"

echo "Image pushed: $IMAGE"
echo "Update Lambda ITC5205-YOLOv5-Kaiser-Container to this image in AWS."
