import socket
from fastapi import FastAPI
from query.routes import results

app = FastAPI()

app.include_router(results.router, prefix = "/query")

@app.get("/")
def health():
    return {
        "status": "LogInsight Query Running",
        "instance": socket.gethostname()
    }