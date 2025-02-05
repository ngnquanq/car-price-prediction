FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder stage
# COPY --from=builder /opt/venv /opt/venv

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy only necessary directories
COPY api/ /app/api/
COPY models/ /app/models/
COPY requirements-inference.txt .

# Install python dep
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m pip install --no-cache-dir -r requirements-inference.txt

# Expose port
EXPOSE 80

# Run the application with Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"] 