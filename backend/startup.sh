#!/bin/bash
# Render startup script - trains model if weights don't exist
set -e

echo "=== MEDCLASSIFY Startup ==="

if [ ! -f "model_weights.pth" ]; then
  echo "Model weights not found. Downloading training data and training..."
  python download_data.py
  python train.py
  echo "Training complete!"
else
  echo "Model weights found. Skipping training."
fi

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
