import json
from common.analyzer import analyze_logs
from common.s3_service import upload_data, upload_with_key
from common.models import StructuredLog


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

    result_payload = {
        "task_id": task_id,
        "result": result,
        "processed_at": "timestamp"
    }

    key = f"results/{task_id}.json"
    upload_with_key(key, result_payload)

    # result_key = upload_data(result_payload)
    print(f"[Processor] Result stored at: {result_key}")

    if structured_logs:
        raw_payload = {
            "task_id": task_id,
            "logs": [log.dict() for log in structured_logs]
        }

        raw_key = upload_data(raw_payload)
        print(f"[Processor] Raw logs stored at: {raw_key}")