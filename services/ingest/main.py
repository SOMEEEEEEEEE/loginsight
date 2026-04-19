import socket
from fastapi import FastAPI
from ingest.routes import logs

app = FastAPI()

app.include_router(logs.router)

@app.get("/")
def health():
    return {
        "status": "LogInsight Ingest Running",
        "instance": socket.gethostname()
    }