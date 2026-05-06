from platform.config.settings import settings
from platform.aws.sqs.client import get_sqs_client

sqs = get_sqs_client()


def receive_messages(max_number: int = 5):
    """
    Receive messages from SQS (long polling).
    """
    response = sqs.receive_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        MaxNumberOfMessages=max_number,
        WaitTimeSeconds=10
    )

    return response.get("Messages", [])


def delete_message(message: dict):
    """
    Delete message after successful processing.
    """
    sqs.delete_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        ReceiptHandle=message["ReceiptHandle"]
    )