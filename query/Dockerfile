FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY query/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY query ./query
COPY common ./common

CMD ["uvicorn", "query.main:app", "--host", "0.0.0.0", "--port", "8002"]