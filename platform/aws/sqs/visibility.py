import boto3

from platform.config.settings import settings

sqs = boto3.client("sqs")


def extend_message_visibility(receipt_handle, message_id, timeout):
    sqs.change_message_visibility(
        QueueUrl=settings.SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle,
        VisibilityTimeout=timeout
    )

    logger.info(
        "Extended message visibility timeout",
        extra={
            "message_id": message_id,
            "visibility_timeout": timeout
        }
    )