import uuid
from ingest.sqs_client import send_message

def enqueue_logs(logs):
    """
    Receives logs and pushes to SQS.
    Does NOT process or store logs directly.
    """
    logs_payload = [log.dict() for log in logs]

    msg_id = send_message(logs_payload)

    return {
        "status": "queued",
        "message_id": msg_id,
        "count": len(logs_payload)
    }


def submit_task(logs):
    """
    Submits logs in batch level for asynchronous analysis.
    Returns a task_id and a message_id for result query.
    """
    task_id = str(uuid.uuid4())

    msg_id = send_message({
        "task_id": task_id,
        "logs": [log.dict() for log in logs]
    })

    return {
        "task_id": task_id,
        "message_id": msg_id
    }