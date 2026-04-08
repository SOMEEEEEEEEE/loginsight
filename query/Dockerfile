FROM python:3.13-slim

WORKDIR /app

COPY query/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY query ./query
COPY common ./common

WORKDIR /app/query

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]