from fastapi import APIRouter
from common.models import LogRequest
from ingest.services.log_service import enqueue_logs

router = APIRouter()

@router.post("/logs")
def ingest_logs(req: LogRequest):
    return enqueue_logs(req.logs)