import os
import json
import time
import boto3
import logging
from worker.processor import process_logs

# --- Configuration ---
AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
QUEUE_URL = os.getenv("SQS_QUEUE_URL")

if not QUEUE_URL:
    raise ValueError("SQS_QUEUE_URL environment variable not set")

# --- Logging setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sqs-worker")

# --- SQS client ---
sqs = boto3.client("sqs", region_name=AWS_REGION)


def handle_message(msg):
    """
    Process a single SQS message safely.
    Delete the message only if processing succeeds.
    """
    try:
        body = json.loads(msg["Body"])

        # Normalize input format
        if isinstance(body, dict) and "logs" in body:
            logs = body["logs"]
        else:
            logs = body

        # Process logs
        process_logs(logs)

        # Delete message after successful processing
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=msg["ReceiptHandle"]
        )

        logger.info("Message processed and deleted successfully")

    except Exception as e:
        # Do NOT delete on failure. Allow retry. 
        logger.error(f"Failed to process message: {e}")


def poll():
    """
    Continuously poll messages from SQS using long polling.
    """
    logger.info("Worker started, polling SQS...")

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=5,      # Batch processing for higher throughput
                WaitTimeSeconds=10,         # Enable long polling
                VisibilityTimeout=30       # Prevent duplicate processing during execution
            )

            messages = response.get("Messages", [])

            if not messages:
                time.sleep(1)
                continue

            for msg in messages:
                handle_message(msg)

        except Exception as e:
            logger.error(f"SQS receive failed: {e}")
            time.sleep(5)  # Prevent tight retry loop


if __name__ == "__main__":
    poll()