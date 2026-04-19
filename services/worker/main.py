import json
import time
from shared.sqs_client import receive_messages, delete_message
from worker.processor import process_logs


def handle_message(msg):
    """
    Process a single SQS message safely.
    Delete only if success.
    """
    try:
        body = json.loads(msg["Body"])

        if not isinstance(body, dict) or "logs" not in body:
            print("[WARN] Invalid message format, skipped")
            return

        process_logs(body)

        delete_message(msg["ReceiptHandle"])

        print("[Worker] Message processed and deleted")

    except Exception as e:
        print(f"[ERROR] Processing failed: {e}")
        print("[ERROR] Raw message:", msg["Body"])


def poll():
    """
    Continuously poll messages from SQS.
    """
    print("[Worker] polling started...")
    while True:
        try:
            messages = receive_messages(max_number=5)

            if not messages:
                time.sleep(1)
                continue

            for msg in messages:
                handle_message(msg)

        except Exception as e:
            print(f"[ERROR] SQS receive failed: {e}")
            time.sleep(5)


if __name__ == "__main__":
    print("worker booting...")
    poll()