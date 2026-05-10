"""
Current improvements:
- Added task_id + message_id tracing for end-to-end observability
- Replaced print with structured logging
- Isolated delete_message failure handling
- Improved metrics granularity for processing lifecycle

Next improvements:
- Add DLQ handling for poison messages
- Introduce SQS long polling + backoff strategy
- Add idempotency control for duplicate messages
"""
import json
import time
from worker.processor import process_logs
from platform.aws.sqs.consumer import delete_message
from platform.metrics.metrics import inc, observe_latency
from platform.logging.logger import get_logger

logger = get_logger("worker_handler")


def handle_message(msg: dict) -> None:
    start = time.time()
    inc("message_received")

    try:
        body = json.loads(msg["Body"])
        task_id = body.get("task_id")

        logger.info(
            "Handling message",
            extra={
                "task_id": task_id,
                "message_id": msg.get("MessageId")
            }
        )

        if "logs" not in body:
            inc("message_invalid")
            raise ValueError("Invalid message format")

        process_logs(body["logs"], task_id=task_id)

        inc("message_success")

        try:
            delete_message(msg)
            inc("message_deleted")
        except Exception:
            inc("message_delete_failed")
            logger.exception(
                "Failed to delete message",
                extra={"task_id": task_id}
            )

    except Exception:
        inc("message_failed")
        logger.exception("Message processing failed")

    finally:
        inc("message_processed")
        observe_latency("message_latency", start)