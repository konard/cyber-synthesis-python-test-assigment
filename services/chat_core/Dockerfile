# Dockerfile for Chat-Core service
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY shared/ ./shared/
COPY services/chat_core/ ./services/chat_core/

ENV PYTHONPATH=/app
EXPOSE 8002

CMD ["uvicorn", "services.chat_core.main:app", "--host", "0.0.0.0", "--port", "8002"]
