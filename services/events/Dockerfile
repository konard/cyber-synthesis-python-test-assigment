# Dockerfile for Events service
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY shared/ ./shared/
COPY services/events/ ./services/events/

ENV PYTHONPATH=/app
EXPOSE 8004

CMD ["uvicorn", "services.events.main:app", "--host", "0.0.0.0", "--port", "8004"]
