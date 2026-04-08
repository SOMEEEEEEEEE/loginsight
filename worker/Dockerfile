FROM python:3.13-slim

WORKDIR /app

COPY worker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY worker ./worker
COPY common ./common

WORKDIR /app/worker

CMD ["python", "main.py"]