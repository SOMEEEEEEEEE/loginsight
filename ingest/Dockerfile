FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY ingest/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ingest ./ingest

COPY common ./common

WORKDIR /app/ingest

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]