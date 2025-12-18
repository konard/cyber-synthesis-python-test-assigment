# Dockerfile for Auth-Match service
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy shared modules and service code
COPY shared/ ./shared/
COPY services/auth_match/ ./services/auth_match/

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8001

# Run the service
CMD ["uvicorn", "services.auth_match.main:app", "--host", "0.0.0.0", "--port", "8001"]
