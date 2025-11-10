"""
Hugging Face Spaces entry point for Innocence-Claim API.
This file serves as the main entry point that Hugging Face Spaces will execute.
"""
import os
import uvicorn
from app.main_bert import app

if __name__ == "__main__":
    # Hugging Face Spaces requires port 7860 (default)
    # Read from PORT environment variable for flexibility
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
