FROM python:3.10

WORKDIR /app

COPY worker/requirements.txt .

RUN pip install -r requirements.txt

COPY common ./common

COPY worker ./worker

WORKDIR /app/worker

CMD ["python", "main.py"]