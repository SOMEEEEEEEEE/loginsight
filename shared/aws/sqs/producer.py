import json
from shared.config.settings import settings
from shared.aws.sqs.client import get_sqs_client

sqs = get_sqs_client()


def send_message(message: dict) -> str:
    """
    Send a message to SQS and return message ID.
    """
    response = sqs.send_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    msg_id = response.get("MessageId")

    if not msg_id:
        raise RuntimeError("Failed to send message to SQS")

    return msg_id