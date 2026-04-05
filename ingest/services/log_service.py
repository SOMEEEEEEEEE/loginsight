import uuid
from common.sqs_client import send_message

def enqueue_logs(logs: list):
    """
    Submit logs to SQS for async processing.
    """

    if not logs:
        return {
            "status": "empty",
            "message": "No logs provided"
        }

    task_id = str(uuid.uuid4())
    logs_payload = [log.dict() for log in logs]

    msg_id = send_message({
        "task_id": task_id,
        "logs": logs_payload
    })

    return {
        "status": "queued",
        "task_id": task_id,
        "message_id": msg_id,
        "count": len(logs_payload),
        "query_hint": f"/results?task_id={task_id}"
    }