---
title: Innocence Claim API
emoji: ⚖️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# Innocence Claim API ⚖️

A FastAPI-based service that analyzes PDF documents to detect and assess innocence claims using a fine-tuned BERT model. The API processes legal documents, extracts sentences, and evaluates their confidence scores to provide reliability metrics.

## Overview

This API uses natural language processing and machine learning to:
- Extract text from PDF documents
- Analyze sentences for innocence claims
- Calculate reliability scores based on confidence thresholds
- Provide tiered assessments (High/Medium/Low)

The model is built on BERT (Bidirectional Encoder Representations from Transformers) and has been fine-tuned specifically for identifying innocence-related statements in legal documents.

## API Endpoints

### POST /predict

Analyzes a PDF document for innocence claims and returns reliability metrics.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Parameters:
  - `file` (required): PDF file to analyze
  - `cutoff` (optional): Confidence threshold (default: 0.7, range: 0.0-1.0)

**Response:**
```json
{
  "reliability_percent": 75.3,
  "tier": "Medium"
}
```

**Example using cURL:**
```bash
curl -X POST https://[your-space-name].hf.space/predict \
  -F "file=@document.pdf" \
  -F "cutoff=0.7"
```

**Example using Python:**
```python
import requests

url = "https://[your-space-name].hf.space/predict"
files = {"file": open("document.pdf", "rb")}
data = {"cutoff": 0.7}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### GET /health

Health check endpoint to verify the API is running.

**Request:**
- Method: `GET`

**Response:**
```json
{
  "status": "ok"
}
```

**Example:**
```bash
curl https://[your-space-name].hf.space/health
```

## Deployment to Hugging Face Spaces

### Prerequisites
- Hugging Face account
- Git installed locally
- Docker (for local testing)

### Step-by-Step Deployment

1. **Create a new Space on Hugging Face:**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name for your Space
   - Select "Docker" as the SDK
   - Set visibility (Public or Private)

2. **Clone your Space repository:**
   ```bash
   git clone https://huggingface.co/spaces/[your-username]/[your-space-name]
   cd [your-space-name]
   ```

3. **Copy the application files:**
   ```bash
   # Copy all necessary files to your Space directory
   cp -r app/ [your-space-name]/
   cp -r models/ [your-space-name]/
   cp app.py [your-space-name]/
   cp Dockerfile [your-space-name]/
   cp requirements.txt [your-space-name]/
   cp start.sh [your-space-name]/
   cp README.md [your-space-name]/
   ```

4. **Handle the model file:**
   
   The `innocence_pipeline.pkl` model file is located in the `models/` directory.
   
   **Option A: Include model in repository (if size < 10MB)**
   ```bash
   git add models/innocence_pipeline.pkl
   ```
   
   **Option B: Use Git LFS for large files (if size > 10MB)**
   ```bash
   # Install Git LFS if not already installed
   git lfs install
   
   # Track the model file with LFS
   git lfs track "models/*.pkl"
   git add .gitattributes
   git add models/innocence_pipeline.pkl
   ```
   
   **Option C: Upload via Hugging Face UI**
   - Navigate to your Space on huggingface.co
   - Click "Files and versions"
   - Click "Add file" → "Upload files"
   - Upload the `innocence_pipeline.pkl` file to the `models/` directory

5. **Commit and push to Hugging Face:**
   ```bash
   git add .
   git commit -m "Initial deployment of Innocence Claim API"
   git push
   ```

6. **Monitor the build:**
   - Go to your Space page on Hugging Face
   - Watch the build logs in the "Logs" tab
   - The build process will:
     - Build the Docker container
     - Install dependencies
     - Download the spaCy model
     - Start the API server on port 7860

7. **Test your deployed API:**
   ```bash
   # Health check
   curl https://[your-username]-[your-space-name].hf.space/health
   
   # Prediction
   curl -X POST https://[your-username]-[your-space-name].hf.space/predict \
     -F "file=@test.pdf" \
     -F "cutoff=0.7"
   ```

### Environment Variables and Secrets

If you need to configure environment variables or secrets:

1. Go to your Space settings on Hugging Face
2. Navigate to "Settings" → "Variables and secrets"
3. Add any required variables (currently none are required for basic operation)

### Model Upload Process

The pre-trained model (`innocence_pipeline.pkl`) contains:
- Fine-tuned BERT tokenizer
- Fine-tuned BERT model weights

**Model size considerations:**
- Check the size of `models/innocence_pipeline.pkl`
- If < 10MB: Include directly in git repository
- If 10MB - 5GB: Use Git LFS (recommended)
- If > 5GB: Consider model compression or hosting externally

## Local Testing

Before deploying to Hugging Face, thoroughly test the application locally to ensure everything works correctly.

### Prerequisites for Local Testing

- Docker installed (version 20.10 or higher recommended)
- At least 2GB free disk space for Docker image
- Sample PDF file for testing
- Terminal/command line access

### Method 1: Testing with Docker (Recommended)

This method replicates the Hugging Face Spaces environment most accurately.

#### Step 1: Build the Docker Image

```bash
docker build -t innocence-api .
```

**Expected output:**
- You should see multiple steps executing (installing Python packages, downloading spaCy model, etc.)
- Build should complete without errors
- Final message: "Successfully tagged innocence-api:latest"

**Build time:** 3-5 minutes on first build (depending on internet speed)

#### Step 2: Run the Container

```bash
docker run -p 7860:7860 innocence-api
```

**Expected output:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
```

**Alternative: Run in detached mode (background)**
```bash
docker run -d -p 7860:7860 --name innocence-api-test innocence-api
```

To view logs:
```bash
docker logs -f innocence-api-test
```

To stop the container:
```bash
docker stop innocence-api-test
docker rm innocence-api-test
```

#### Step 3: Test the Health Endpoint

Open a new terminal and run:

```bash
curl http://localhost:7860/health
```

**Expected response:**
```json
{"status":"ok"}
```

**Alternative: Test in browser**
- Open http://localhost:7860/health in your web browser
- You should see the JSON response

#### Step 4: Test the Prediction Endpoint

**Basic test with default cutoff (0.7):**
```bash
curl -X POST http://localhost:7860/predict \
  -F "file=@path/to/your/test.pdf"
```

**Test with custom cutoff:**
```bash
curl -X POST http://localhost:7860/predict \
  -F "file=@path/to/your/test.pdf" \
  -F "cutoff=0.8"
```

**Expected response:**
```json
{
  "reliability_percent": 75.3,
  "tier": "Medium"
}
```

**Test with verbose output:**
```bash
curl -v -X POST http://localhost:7860/predict \
  -F "file=@path/to/your/test.pdf" \
  -F "cutoff=0.7"
```

**Test different cutoff values:**
```bash
# High confidence threshold
curl -X POST http://localhost:7860/predict \
  -F "file=@test.pdf" \
  -F "cutoff=0.9"

# Low confidence threshold
curl -X POST http://localhost:7860/predict \
  -F "file=@test.pdf" \
  -F "cutoff=0.5"

# Edge cases
curl -X POST http://localhost:7860/predict \
  -F "file=@test.pdf" \
  -F "cutoff=0.0"

curl -X POST http://localhost:7860/predict \
  -F "file=@test.pdf" \
  -F "cutoff=1.0"
```

#### Step 5: Test Error Handling

**Test with non-PDF file:**
```bash
curl -X POST http://localhost:7860/predict \
  -F "file=@test.txt" \
  -F "cutoff=0.7"
```

**Expected response:**
```json
{
  "detail": "PDF required"
}
```

**Test with missing file:**
```bash
curl -X POST http://localhost:7860/predict \
  -F "cutoff=0.7"
```

**Test with invalid cutoff:**
```bash
curl -X POST http://localhost:7860/predict \
  -F "file=@test.pdf" \
  -F "cutoff=invalid"
```

### Method 2: Testing with Python Directly

This method is faster for development but doesn't test the Docker configuration.

#### Step 1: Set Up Python Environment

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

#### Step 2: Verify Model File Exists

```bash
ls -lh models/innocence_pipeline.pkl
```

You should see the model file with its size. If missing, the application will fail to start.

#### Step 3: Run the Application

```bash
python app.py
```

**Expected output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
```

#### Step 4: Test Endpoints

Use the same curl commands as in Method 1, Step 3 and Step 4.

### Method 3: Testing with Python Requests Library

Create a test script `test_api.py`:

```python
import requests
import sys

def test_health():
    """Test the health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get("http://localhost:7860/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✓ Health check passed\n")

def test_predict(pdf_path, cutoff=0.7):
    """Test the predict endpoint"""
    print(f"Testing /predict endpoint with {pdf_path}...")
    with open(pdf_path, "rb") as f:
        files = {"file": f}
        data = {"cutoff": cutoff}
        response = requests.post("http://localhost:7860/predict", files=files, data=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        result = response.json()
        assert "reliability_percent" in result
        assert "tier" in result
        assert result["tier"] in ["High", "Medium", "Low"]
        print("✓ Prediction test passed\n")
    else:
        print("✗ Prediction test failed\n")
        return False
    return True

def test_error_handling():
    """Test error handling with invalid input"""
    print("Testing error handling...")
    
    # Test with missing file
    response = requests.post("http://localhost:7860/predict", data={"cutoff": 0.7})
    print(f"Missing file - Status Code: {response.status_code}")
    assert response.status_code == 422  # Unprocessable Entity
    print("✓ Missing file handling passed\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <path_to_test_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    try:
        test_health()
        test_predict(pdf_path)
        test_predict(pdf_path, cutoff=0.9)
        test_error_handling()
        print("All tests passed! ✓")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
```

Run the test script:
```bash
python test_api.py path/to/test.pdf
```

### Performance Testing

#### Test Response Times

```bash
# Test cold start (first request)
time curl -X POST http://localhost:7860/predict \
  -F "file=@test.pdf" \
  -F "cutoff=0.7"

# Test warm request (subsequent requests)
time curl -X POST http://localhost:7860/predict \
  -F "file=@test.pdf" \
  -F "cutoff=0.7"
```

#### Test with Different PDF Sizes

```bash
# Small PDF (1-5 pages)
time curl -X POST http://localhost:7860/predict -F "file=@small.pdf"

# Medium PDF (10-20 pages)
time curl -X POST http://localhost:7860/predict -F "file=@medium.pdf"

# Large PDF (50+ pages)
time curl -X POST http://localhost:7860/predict -F "file=@large.pdf"
```

### Troubleshooting Local Testing Issues

#### Issue: Docker build fails with "No space left on device"

**Symptoms:**
```
ERROR: failed to solve: write /var/lib/docker/...: no space left on device
```

**Solutions:**
1. Clean up Docker resources:
   ```bash
   docker system prune -a
   docker volume prune
   ```

2. Check available disk space:
   ```bash
   df -h
   ```

3. Remove unused Docker images:
   ```bash
   docker images
   docker rmi <image-id>
   ```

#### Issue: Port 7860 already in use

**Symptoms:**
```
Error: bind: address already in use
```

**Solutions:**
1. Find and stop the process using port 7860:
   ```bash
   # On macOS/Linux
   lsof -i :7860
   kill -9 <PID>
   
   # On Windows
   netstat -ano | findstr :7860
   taskkill /PID <PID> /F
   ```

2. Use a different port:
   ```bash
   docker run -p 8080:7860 innocence-api
   # Then test with: curl http://localhost:8080/health
   ```

#### Issue: Model file not found

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/innocence_pipeline.pkl'
```

**Solutions:**
1. Verify model file exists:
   ```bash
   ls -la models/
   ```

2. Check if Git LFS is needed:
   ```bash
   file models/innocence_pipeline.pkl
   # If it shows "ASCII text", it's an LFS pointer, not the actual file
   ```

3. Pull LFS files:
   ```bash
   git lfs pull
   ```

4. Rebuild Docker image after ensuring model is present:
   ```bash
   docker build --no-cache -t innocence-api .
   ```

#### Issue: spaCy model download fails

**Symptoms:**
```
OSError: [E050] Can't find model 'en_core_web_sm'
```

**Solutions:**
1. Manually download the model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. Check internet connectivity during Docker build

3. Use a mirror or download the model separately:
   ```bash
   pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
   ```

#### Issue: Container starts but API doesn't respond

**Symptoms:**
- Container is running but curl requests timeout or fail
- No error messages in logs

**Solutions:**
1. Check container logs:
   ```bash
   docker logs innocence-api-test
   ```

2. Verify container is running:
   ```bash
   docker ps
   ```

3. Check if the application is listening on the correct port:
   ```bash
   docker exec innocence-api-test netstat -tuln | grep 7860
   ```

4. Test from inside the container:
   ```bash
   docker exec innocence-api-test curl http://localhost:7860/health
   ```

5. Restart the container:
   ```bash
   docker restart innocence-api-test
   ```

#### Issue: PDF processing fails or returns errors

**Symptoms:**
```
{"detail": "Internal server error"}
```

**Solutions:**
1. Check if PDF is valid:
   ```bash
   file test.pdf
   # Should show: "PDF document, version X.X"
   ```

2. Try with a different PDF file

3. Check container logs for detailed error:
   ```bash
   docker logs innocence-api-test
   ```

4. Test with a simple PDF:
   - Create a test PDF with just a few sentences
   - Verify it processes successfully

5. Check PDF text extraction:
   ```python
   import pdfplumber
   with pdfplumber.open("test.pdf") as pdf:
       for page in pdf.pages:
           print(page.extract_text())
   ```

#### Issue: Slow prediction times

**Symptoms:**
- Requests take more than 30 seconds
- Timeout errors

**Solutions:**
1. Check PDF size and page count:
   ```bash
   pdfinfo test.pdf  # If pdfinfo is installed
   ```

2. Test with smaller PDFs first

3. Monitor resource usage:
   ```bash
   docker stats innocence-api-test
   ```

4. Increase Docker memory allocation (Docker Desktop settings)

5. Consider using GPU acceleration for faster inference (requires CUDA setup)

#### Issue: CORS errors when testing from browser

**Symptoms:**
```
Access to fetch at 'http://localhost:7860/predict' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solutions:**
1. Check CORS configuration in `app/main_bert.py`

2. Verify allowed origins include your test origin

3. Use curl or Postman instead of browser for testing

4. Add your origin to CORS middleware temporarily for testing

#### Issue: Dependencies fail to install

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement torch==X.X.X
```

**Solutions:**
1. Check Python version:
   ```bash
   python --version
   # Should be 3.11 or compatible with requirements.txt
   ```

2. Update pip:
   ```bash
   pip install --upgrade pip
   ```

3. Install dependencies one by one to identify the problematic package:
   ```bash
   pip install torch
   pip install transformers
   # etc.
   ```

4. Check for platform-specific issues (especially with PyTorch on different OS)

### Validation Checklist

Before deploying to Hugging Face, ensure:

- [ ] Docker image builds successfully without errors
- [ ] Container starts and shows "Uvicorn running" message
- [ ] `/health` endpoint returns `{"status":"ok"}`
- [ ] `/predict` endpoint accepts PDF and returns valid JSON
- [ ] Different cutoff values (0.5, 0.7, 0.9) work correctly
- [ ] Error handling works (non-PDF file returns 400 error)
- [ ] Model loads correctly (check logs for model loading messages)
- [ ] Response times are reasonable (< 30 seconds for small PDFs)
- [ ] No error messages in Docker logs during normal operation
- [ ] Container can be stopped and restarted without issues

### Next Steps After Successful Local Testing

Once all local tests pass:

1. Commit your changes to git
2. Push to Hugging Face Spaces repository
3. Monitor the build logs on Hugging Face
4. Test the deployed API using the Hugging Face Space URL
5. Compare local and deployed behavior to ensure consistency

## Technical Details

### Dependencies
- **FastAPI**: Web framework for building the API
- **PyTorch**: Deep learning framework for running the BERT model
- **Transformers**: Hugging Face library for BERT tokenizer and model
- **pdfplumber**: PDF text extraction
- **spaCy**: Natural language processing for sentence segmentation
- **uvicorn**: ASGI server for running FastAPI

### Model Architecture
- Base model: BERT (Bidirectional Encoder Representations from Transformers)
- Task: Binary classification (innocence claim detection)
- Input: Text sentences (max 128 tokens)
- Output: Confidence score (0.0 - 1.0)

### Processing Pipeline
1. Extract text from PDF pages using pdfplumber
2. Segment text into sentences using spaCy
3. Filter sentences (length between 10-500 characters)
4. Tokenize and encode sentences using BERT tokenizer
5. Run inference with fine-tuned BERT model
6. Calculate confidence scores and aggregate metrics
7. Return reliability percentage and tier classification

## Limitations and Considerations

- **Cold starts**: First request after inactivity may take 30-60 seconds as the model loads
- **Processing time**: Large PDFs (>50 pages) may take several minutes to process
- **Memory usage**: The BERT model requires ~500MB RAM minimum
- **Concurrent requests**: Free tier Spaces have limited concurrency (1-2 requests)
- **Timeout**: Very large documents may timeout on free tier (consider upgrading to paid tier)
- **GPU support**: Currently configured for CPU inference (GPU can be enabled in paid tiers)

## Troubleshooting

### Build fails with "No space left on device"
- The Docker image may be too large
- Consider removing unnecessary files or using a smaller base image

### Model fails to load
- Verify `models/innocence_pipeline.pkl` exists and is not corrupted
- Check that Git LFS properly tracked and uploaded the file
- Review build logs for pickle/torch loading errors

### API returns 400 "PDF required"
- Ensure you're sending `Content-Type: multipart/form-data`
- Verify the file parameter is named `file`
- Check that the uploaded file is a valid PDF

### Slow response times
- First request (cold start) is always slower
- Consider upgrading to a paid tier for better performance
- Optimize the model or use quantization for faster inference

## Support and Contributing

For issues, questions, or contributions, please visit the Space's discussion page or repository.

## License

[Add your license information here]
