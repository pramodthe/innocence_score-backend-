FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model (verify installation)
RUN python -m spacy download en_core_web_sm && \
    python -c "import spacy; spacy.load('en_core_web_sm'); print('✓ Spacy model loaded successfully')"

# Copy application code
COPY . .

# Ensure start.sh is executable
RUN chmod +x start.sh && \
    test -x start.sh && \
    echo "✓ start.sh is executable"

# Create models directory if it doesn't exist
RUN mkdir -p models

# Set environment variables for Hugging Face Spaces
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Expose port (Hugging Face Spaces requirement)
EXPOSE 7860

# Health check to verify the service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:7860/health || exit 1

# Run the application with startup script
CMD ["./start.sh"]
