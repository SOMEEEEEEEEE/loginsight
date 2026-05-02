import json
from shared.sqs_client import delete_message
from worker.processor import process_logs


def handle_message(msg):
    try:
        body = json.loads(msg["Body"])

        if "logs" not in body:
            raise ValueError("Invalid message format")

        process_logs(body["logs"])

        delete_message(msg)

    except Exception as e:
        print(f"[ERROR] Failed processing message: {e}")