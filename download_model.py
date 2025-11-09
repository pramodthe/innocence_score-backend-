"""
Download the model file during build or startup.
Set MODEL_URL environment variable.
"""
import os
import urllib.request
from pathlib import Path
import sys

def download_model():
    model_url = os.getenv("MODEL_URL")
    if not model_url:
        print("⚠️  MODEL_URL not set. Skipping model download.")
        print("⚠️  App will fail if model file doesn't exist!")
        return False
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / "innocence_pipeline.pkl"
    
    if model_path.exists():
        file_size = model_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ Model already exists at {model_path} ({file_size:.1f} MB)")
        return True
    
    print(f"📥 Downloading model from {model_url}...")
    try:
        urllib.request.urlretrieve(model_url, model_path)
        file_size = model_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ Model downloaded to {model_path} ({file_size:.1f} MB)")
        return True
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
