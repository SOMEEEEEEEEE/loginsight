FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY services/worker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY shared /app/shared
COPY services/worker /app/worker

CMD ["python", "-u", "-m", "worker.main"]