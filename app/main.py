from fastapi import FastAPI
from pydantic import BaseModel
from app.analyzer import analyze_logs

app = FastAPI()

class LogRequest(BaseModel):
    logs: list[str]

# Health check endpoint
@app.get("/")
def health():
    return {"status": "ok"}

# Analyze endpoint: receives logs and returns analysis
@app.post("/analyze")
def analyze(req: LogRequest):
    result = analyze_logs(req.logs)
    return result