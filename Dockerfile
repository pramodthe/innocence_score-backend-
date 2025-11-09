FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Download the ML model at build time
RUN python download_model.py

# Expose port
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD uvicorn app.main_bert:app --host 0.0.0.0 --port $PORT
