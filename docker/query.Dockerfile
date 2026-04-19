FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY services/query/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY shared /app/shared
COPY services/query /app/services/query

WORKDIR /app/services/query

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]