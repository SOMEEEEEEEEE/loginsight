import json
from worker.models import StructuredLog
from common.analyzer import analyze_logs
from common.s3_client import upload_log


def process_logs(logs):
    """
    Process logs: analyze and upload to S3.
    logs: list of dicts
    """
    print(f"[Processor] Processing {len(logs)} logs...")

    structured_logs = []
    for log in logs:
        try:
            structured_logs.append(StructuredLog(**log))
        except Exception as e:
            print(f"[WARN] Bad log skipped: {e}")

    analyze_logs(structured_logs)

    for log in structured_logs:
        upload_log(log.dict())