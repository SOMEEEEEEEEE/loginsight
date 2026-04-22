FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY services/ingest/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY shared /app/shared
COPY services/ingest /app/ingest

CMD ["uvicorn", "ingest.main:app", "--host", "0.0.0.0", "--port", "8000"]