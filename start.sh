#!/bin/bash
set -e

echo "🚀 Starting Innocence API..."

# Download model if MODEL_URL is set
if [ -n "$MODEL_URL" ]; then
    echo "📥 Downloading model..."
    python download_model.py
else
    echo "⚠️  MODEL_URL not set, expecting model to be in container"
fi

# Start the application
echo "🌐 Starting uvicorn server on port $PORT..."
exec uvicorn app.main_bert:app --host 0.0.0.0 --port $PORT
