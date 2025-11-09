#!/bin/bash

# Google Cloud deployment script for Innocence API

set -e

echo "🚀 Deploying Innocence API to Google Cloud Run..."

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-your-project-id}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="innocence-api"
MODEL_URL="${MODEL_URL}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if MODEL_URL is set
if [ -z "$MODEL_URL" ]; then
    echo "⚠️  MODEL_URL environment variable not set"
    echo "Set it with: export MODEL_URL='your-model-download-url'"
fi

# Set project
echo "📦 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
echo "🏗️  Building and deploying..."
gcloud builds submit --config cloudbuild.yaml \
    --substitutions=_MODEL_URL="$MODEL_URL"

echo "✅ Deployment complete!"
echo "🌐 Your API is available at:"
gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)'
