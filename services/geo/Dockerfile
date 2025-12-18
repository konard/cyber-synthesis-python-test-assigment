# Dockerfile for Geo service
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY shared/ ./shared/
COPY services/geo/ ./services/geo/

ENV PYTHONPATH=/app
EXPOSE 8005

CMD ["uvicorn", "services.geo.main:app", "--host", "0.0.0.0", "--port", "8005"]
