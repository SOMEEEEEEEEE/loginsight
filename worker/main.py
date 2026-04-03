import os
import json
import time
import boto3
from worker.processor import process_logs

AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
QUEUE_URL = os.getenv("SQS_QUEUE_URL")

if not QUEUE_URL:
    raise ValueError("SQS_QUEUE_URL environment variable not set")

sqs = boto3.client("sqs", region_name=AWS_REGION)


while True:
    try:
        # Listening to SQS via long polling
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )

        messages = response.get("Messages", [])

        for msg in messages:
            try:
                body = json.loads(msg["Body"])

                if isinstance(body, dict) and "logs" in body:
                    logs = body["logs"]
                else:
                    logs = body

                process_logs(body)

                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print(f"[ERROR] Failed to process message: {e}")

        if not messages:
            time.sleep(1)

    except Exception as e:
        print(f"[ERROR] SQS receive failed: {e}")
        time.sleep(5)