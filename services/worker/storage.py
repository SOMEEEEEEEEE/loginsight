"""
Initialization: Decoupled data storage from processor.py for a clearer structure
"""
import json
from datetime import datetime
from botocore.exceptions import ClientError

from platform.config.settings import settings
from platform.aws.s3.service import upload_with_key, upload_data
from platform.logging.logger import get_logger
from platform.metrics.metrics import inc, observe_latency

logger = get_logger("worker_storage")

def save_result(task_id: str, result: dict) -> str:
    start = datetime.utcnow()

    key = f"results/{task_id}.json"

    payload = {
        "task_id": task_id,
        "result": result,
        "processed_at": datetime.utcnow().isoformat()
    }

    try:
        upload_with_key(key, payload)
        inc("s3_upload_success")

        return key

    except ClientError:
        inc("s3_upload_failed")
        logger.exception("S3 result upload failed", extra={"task_id": task_id, "key": key})
        raise

    finally:
        observe_latency("s3_upload_latency", start)


def save_raw(task_id: str, logs: list) -> str:
    start = datetime.utcnow()

    payload = {
        "task_id": task_id,
        "logs": [log.dict() for log in logs]
    }

    try:
        key = upload_data(payload)
        inc("s3_upload_success")

        return key

    except ClientError:
        inc("s3_upload_failed")
        logger.exception("S3 raw upload failed", extra={"task_id": task_id})
        raise

    finally:
        observe_latency("s3_upload_latency", start)