FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY worker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY worker ./worker
COPY common ./common

CMD ["python", "-u", "worker/main.py"]