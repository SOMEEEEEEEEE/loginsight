import socket
from fastapi import FastAPI

from api.sqs_client import send_message
from api.models import LogRequest, StructuredLog

app = FastAPI()


# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def health():
    return {
        "status": "LogInsight Running",
        "instance": socket.gethostname()
    }


# ----------------------------
# Ingest Logs (Async via SQS)
# ----------------------------
@app.post("/logs")
def ingest_logs(req: LogRequest):
    """
    Receives logs and pushes them to SQS.
    Does NOT process or store logs directly.
    """

    # Convert to dict for json serializing
    logs_payload = [log.dict() for log in req.logs]

    # Send to SQS
    send_message(logs_payload)

    return {
        "status": "queued",
        "count": len(logs_payload)
    }