# FALCON-Q: IBM Qiskit Fall Fest 2026 Problem Statement VNQFF-04 Production Container
# Quantum Multimodal Crop Disease Early Warning Platform
# Team TISSOT

FROM python:3.11-slim-bookworm

WORKDIR /app

# Install essential system dependencies for OpenCV and image operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
        torch==2.2.2+cpu torchvision==0.17.2+cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure static/uploads directory exists
RUN mkdir -p /app/static/uploads

# Expose REST API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/config/taxonomy || exit 1

# Production server entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
