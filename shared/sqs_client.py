import boto3
import os
import json

AWS_REGION = os.getenv("AWS_REGION")
QUEUE_URL = os.getenv("SQS_QUEUE_URL")

if not QUEUE_URL:
    raise ValueError("SQS_QUEUE_URL not set")

if not AWS_REGION:
    raise ValueError("AWS_REGION not set")

sqs = boto3.client("sqs", region_name=AWS_REGION)


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


def receive_messages(max_number: int = 1):
    """
    Receive messages from SQS.
    """
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=max_number,
        WaitTimeSeconds=10
    )

    return response.get("Messages", [])


def delete_message(receipt_handle: str):
    """
    Delete message from SQS after processing.
    """
    sqs.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=receipt_handle
    )