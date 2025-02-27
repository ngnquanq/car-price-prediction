FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy necessary directories and files
COPY api/ /app/api/
COPY models/ /app/models/
COPY requirements-inference.txt .
COPY start.sh /app/start.sh

# Create a Python virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m pip install --no-cache-dir -r requirements-inference.txt

# Pre-create the log directory with proper permissions.
# Note: In Kubernetes, this directory will be overlaid by the emptyDir volume,
# but setting it up here ensures the image is prepared for local testing.
RUN mkdir -p /var/log/myapp && chmod -R 777 /var/log/myapp

# Expose port 80
EXPOSE 80

# Run the application with Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
