#!/usr/bin/env bash
set -e
API="https://rr5ia59noc.execute-api.us-east-1.amazonaws.com/detect"

echo "Single request:"
curl -s -X POST "$API"
echo

echo "Five concurrent requests:"
for i in {1..5}; do
  curl -s -X POST "$API" &
done
wait
echo
