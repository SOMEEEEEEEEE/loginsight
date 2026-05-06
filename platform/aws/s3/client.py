# shared/aws/s3/client.py

import boto3
from platform.config.settings import settings


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def put_object(bucket: str, key: str, body: bytes, content_type="application/json"):
    return s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType=content_type
    )


def get_object(bucket: str, key: str):
    return s3.get_object(Bucket=bucket, Key=key)