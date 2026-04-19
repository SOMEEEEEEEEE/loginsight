import boto3
import os

AWS_REGION = os.getenv("AWS_REGION")
BUCKET = os.getenv("S3_BUCKET")

if not AWS_REGION:
    raise ValueError("AWS_REGION environment variable not set")

if not BUCKET:
    raise ValueError("S3_BUCKET environment variable not set")

s3 = boto3.client("s3", region_name=AWS_REGION)