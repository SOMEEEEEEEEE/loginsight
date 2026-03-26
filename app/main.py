from fastapi import FastAPI
from pydantic import BaseModel
from app.analyzer import analyze_logs

app = FastAPI()

logs_storage = []

class LogRequest(BaseModel):
    logs: list[str]

# Health check
@app.get("/")
def health():
    return {"status": "LogInsight running"}

# Ingest logs: save uploaded logs and returns status
@app.post("/ingest")
def ingest(req: LogRequest):
    logs_storage.extend(req.logs)
    return {"msg": f"{len(req.logs)} logs ingested", "total_logs": len(logs_storage)}

# Analyze logs: receives logs and returns analysis
@app.get("/analyze")
def analyze():
    if not logs_storage:
        return {"msg": "No logs ingested yet"}
    result = analyze_logs(logs_storage)
    return result

# Reset logs: clears all historical logs when necessary
@app.post("/reset")
def reset():
    logs_storage.clear()
    return {"msg": "All logs cleared"}