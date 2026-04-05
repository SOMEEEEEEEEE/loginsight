from fastapi import APIRouter
from common.models import LogRequest
from ingest.services.log_service import enqueue_logs, submit_task

router = APIRouter()

@router.post("/ingest")
def ingest_logs(req: LogRequest):
    return enqueue_logs(req.logs)


@router.post("/submit")
def submit_logs(req: LogRequest):
    return submit_task(req.logs)