# Dockerfile for Social-Feed service
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY shared/ ./shared/
COPY services/social_feed/ ./services/social_feed/

ENV PYTHONPATH=/app
EXPOSE 8003

CMD ["uvicorn", "services.social_feed.main:app", "--host", "0.0.0.0", "--port", "8003"]
