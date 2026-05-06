from fastapi import APIRouter
from ingest.services.log_service import enqueue_logs
from platform.contracts.log_request import LogRequest


router = APIRouter()

@router.post("/logs")
def ingest_logs(req: LogRequest):
    return enqueue_logs(req.logs)