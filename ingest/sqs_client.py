import boto3
import os
import json

## Create SQS client
sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION"))

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

if not QUEUE_URL:
    raise ValueError("SQS_QUEUE_URL not set")

def send_message(message: dict) -> str:
    """
    Send a message to SQS and return message ID. 

    message example:
    {
        "task_id": "...",
        "logs": [...]
    }
    """
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    msg_id = response.get("MessageId")

    if not msg_id:
        raise RuntimeError("Failed to send message to SQS")

    return msg_id