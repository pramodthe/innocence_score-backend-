#!/bin/bash
set -e

echo "🚀 Starting Innocence API..."

# Verify model file exists
MODEL_PATH="models/innocence_pipeline.pkl"
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Error: Model file not found at $MODEL_PATH"
    echo "   Please ensure the model is included in the container or set MODEL_URL"
    exit 1
fi

MODEL_SIZE=$(du -h "$MODEL_PATH" | cut -f1)
echo "✓ Model file found: $MODEL_PATH ($MODEL_SIZE)"

# Set default port to 7860 for Hugging Face Spaces
PORT=${PORT:-7860}

# Start the application
echo "🌐 Starting uvicorn server on 0.0.0.0:$PORT..."
exec uvicorn app.main_bert:app --host 0.0.0.0 --port $PORT
