"""
Download the model file during Render build process.
Set MODEL_URL environment variable in Render dashboard.
"""
import os
import urllib.request
from pathlib import Path

def download_model():
    model_url = os.getenv("MODEL_URL")
    if not model_url:
        print("⚠️  MODEL_URL not set. Skipping model download.")
        return
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / "innocence_pipeline.pkl"
    
    if model_path.exists():
        print(f"✓ Model already exists at {model_path}")
        return
    
    print(f"Downloading model from {model_url}...")
    urllib.request.urlretrieve(model_url, model_path)
    print(f"✓ Model downloaded to {model_path}")

if __name__ == "__main__":
    download_model()
