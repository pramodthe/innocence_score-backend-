# Deploy to Google Cloud Run

## Prerequisites

1. **Install Google Cloud SDK**
   ```bash
   # macOS
   brew install --cask google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

3. **Create a Google Cloud Project** (if you don't have one)
   - Go to: https://console.cloud.google.com/
   - Create a new project or select existing one
   - Note your PROJECT_ID

## Option 1: Upload Model to Google Cloud Storage (Recommended)

```bash
# Create a bucket
gsutil mb gs://your-bucket-name

# Upload your model
gsutil cp models/innocence_pipeline.pkl gs://your-bucket-name/

# Make it publicly readable (or use signed URLs for private access)
gsutil acl ch -u AllUsers:R gs://your-bucket-name/innocence_pipeline.pkl

# Get the public URL
echo "https://storage.googleapis.com/your-bucket-name/innocence_pipeline.pkl"
```

## Option 2: Deploy with Model in Container

If your model is small enough or you want to include it in the Docker image:

1. Remove `models/innocence_pipeline.pkl` from `.gitignore`
2. Comment out the `RUN python download_model.py` line in Dockerfile
3. The model will be baked into the container image

## Deploy to Cloud Run

### Method 1: Using the deploy script

```bash
# Set your project ID
export GCP_PROJECT_ID="your-project-id"

# Set model URL (if using Cloud Storage)
export MODEL_URL="https://storage.googleapis.com/your-bucket-name/innocence_pipeline.pkl"

# Deploy
./deploy.sh
```

### Method 2: Manual deployment

```bash
# Set project
gcloud config set project your-project-id

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Build and deploy
gcloud builds submit --tag gcr.io/your-project-id/innocence-api

# Deploy to Cloud Run
gcloud run deploy innocence-api \
  --image gcr.io/your-project-id/innocence-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars MODEL_URL="your-model-url"
```

## Test Your Deployment

```bash
# Get your service URL
SERVICE_URL=$(gcloud run services describe innocence-api --region=us-central1 --format='value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health

# Test prediction (with a PDF file)
curl -X POST "$SERVICE_URL/predict" \
  -F "file=@test.pdf" \
  -F "cutoff=0.7"
```

## Costs

- Cloud Run: Pay per request (free tier: 2M requests/month)
- Cloud Storage: ~$0.02/GB/month
- Cloud Build: 120 build-minutes/day free

## Troubleshooting

View logs:
```bash
gcloud run services logs read innocence-api --region=us-central1
```

Check service status:
```bash
gcloud run services describe innocence-api --region=us-central1
```
