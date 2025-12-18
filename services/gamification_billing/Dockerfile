# Dockerfile for Gamification & Billing service
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY shared/ ./shared/
COPY services/gamification_billing/ ./services/gamification_billing/

ENV PYTHONPATH=/app
EXPOSE 8006

CMD ["uvicorn", "services.gamification_billing.main:app", "--host", "0.0.0.0", "--port", "8006"]
