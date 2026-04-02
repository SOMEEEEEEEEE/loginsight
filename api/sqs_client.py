import boto3
import os
import json

## Create SQS client
sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION"))

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

def send_message(logs):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(logs)
    )