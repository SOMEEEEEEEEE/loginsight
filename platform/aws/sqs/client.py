import boto3
from platform.config.settings import settings


def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=settings.AWS_REGION
    )