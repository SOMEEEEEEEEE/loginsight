from fastapi import FastAPI
from pydantic import BaseModel
from app.analyzer import analyze_logs
from app.s3_client import upload_log, get_all_logs, delete_all_logs
from typing import Optional
import json


app = FastAPI()


class StructuredLog(BaseModel):
    timestamp: str
    level: str
    message: str
    service: Optional[str] = None


class LogRequest(BaseModel):
    logs: list[StructuredLog]




# Health check
@app.get("/")
def health():
    return {"status": "LogInsight running"}


# Ingest logs: saves uploaded structured logs into S3 bucket and returns status
@app.post("/ingest")
def ingest(req: LogRequest):
    keys = []

    for log in req.logs:
        key = upload_log(log.json())  # converted to JSON str
        keys.append(key)

    return {
        "msg": f"{len(req.logs)} logs ingested",
        "s3_keys": keys
    }


# Analyze logs: receives logs and returns analysis
@app.get("/analyze")
def analyze():
    raw_logs = get_all_logs()

    if not raw_logs:
        return {"msg": "No logs in S3"}

    logs = [StructuredLog(**json.loads(log)) for log in raw_logs]

    result = analyze_logs(logs)
    return result


# Reset logs: clears all historical logs when necessary
@app.post("/reset")
def reset():
    delete_all_logs()
    return {"msg": "All logs deleted from S3"}