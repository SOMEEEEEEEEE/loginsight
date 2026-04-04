import json
from common.analyzer import analyze_logs
from common.s3_client import upload_result, upload_log
from worker.models import StructuredLog


def process_logs(data: dict):
    """
    Process a batch of logs: analyze and upload results at task level.
    data: dict with 'task_id' and 'logs'
    """
    task_id = data.get("task_id")
    logs = data.get("logs", [])

    print(f"[Processor] Processing {len(logs)} logs for task_id={task_id}...")

    structured_logs = []
    for log in logs:
        try:
            structured_logs.append(StructuredLog(**log))
        except Exception as e:
            print(f"[WARN] Bad log skipped: {e}")

    # Batch-level analysis
    result = analyze_logs(structured_logs)

    # Store batch-level result
    if task_id:
        upload_result(task_id, result)

    # Optionally store raw logs
    if structured_logs:
        upload_log({
            "task_id": task_id,
            "logs": [log.dict() for log in structured_logs]
        })